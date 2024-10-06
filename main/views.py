import json
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import UserRegistrationForm, LoginForm
from .models import Cartoons, CartoonsTypes, CartoonsStatus, CartoonsGenres, User, Profile
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Q
from django.http import QueryDict
from myList.models import MyListStatus, MyListScores, MyListObject
from django.core.exceptions import PermissionDenied
from django.views.decorators.http import require_POST

words_replace = {
    'sort': {
        'popularity': 'number_of_ratings',
        'release': 'start_year',
        'title': 'rus_title'
    }
}
allowed_get = ['sort', 'status', 'type', 'genres', 'studios']

def index(request):
    return redirect('cartoons/')

def show_cartoons(request):
    checked_queries = {}

    for key in request.GET:
        if key in allowed_get:
            checked_queries[key] = request.GET.get(key)
    
    queries = []
    for key in checked_queries:
        if key == 'sort':
            for i in words_replace['sort']:
                checked_queries[key] = checked_queries[key].replace(i, words_replace['sort'][i])
            continue

        if key == 'page':
            continue

        val = checked_queries[key]
        tq =  []
        if key in ['studios']:
            queries.append(["or", [[key + '__name', val]]])
            continue
        for i in val.split(","):
            tq.append([key + "__eng_name", i])
        if key == "genres":
            queries.append(["and", tq])
            continue

        queries.append(["or", tq])     
    # GET queries 

    filters = Q()
    filterWithAnd = []
    if queries:
        for qur in queries:
            fq = Q()
            if qur[0] == "or":
                for q in qur[1]:
                    fq |= Q(**{q[0]:q[1]})
            elif qur[0] == "and":
                for q in qur[1]:
                    filterWithAnd.append(Q(**{q[0]: q[1]}))
            
            filters &= fq
    
    cartoons = Cartoons.objects.filter(filters).distinct()
    for i in filterWithAnd:
        cartoons = cartoons.filter(i)

    sortBy = checked_queries.get('sort')
    if sortBy:
        try:
            cartoons = cartoons.order_by(sortBy)[::-1] # Заменяет -rating на rating и наоборот
        except:
            return redirect('cartoons')
    
    paginator = Paginator(cartoons, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.GET.get('cartoons_only'):
        return render(request, 'main/cartoons_only.html', {
            "page_obj": page_obj
        })

    cartoon_satus = CartoonsStatus.objects.all()
    cartoon_types = CartoonsTypes.objects.all()
    cartoon_genres = CartoonsGenres.objects.all()

    query_params = QueryDict('', mutable=True)
    query_params.update(request.GET)

    if not page_number:
        page_number = 1
    query_params['page'] = int(page_number) + 1
    next_page_url = f"?{query_params.urlencode()}"
    query_params['page'] -= 2
    prev_page_url = f"?{query_params.urlencode()}"

    data = {
        "page_obj": page_obj,
        "c_status": cartoon_satus,
        "c_types": cartoon_types,
        "c_genres": cartoon_genres,
        "prev_page": prev_page_url, 
        "next_page": next_page_url
    }
    return render(request, 'main/cartoons.html', data)

def show_cartoon_page(request, cartoon_id, cartoon_name=None):
    cartoon = get_object_or_404(Cartoons, id=cartoon_id)

    ml_cartoon_info = MyListObject.objects.filter(cartoon__id=cartoon_id, user__id=request.user.id)
    
    if ml_cartoon_info:
        ml_cartoon_info = ml_cartoon_info[0]
    else:
        ml_cartoon_info = None

    seasons_word = ""
    series_word = ""

    if cartoon.number_of_seasons:
        if cartoon.number_of_seasons % 10 == 1 and cartoon.number_of_seasons != 11:
            seasons_word = "сезон"
        elif cartoon.number_of_seasons % 10 in [2, 3, 4] and cartoon.number_of_seasons not in [11, 12, 13, 14]:
            seasons_word = "сезона"
        else:
            seasons_word = "сезонов"


    if cartoon.number_of_series:
        if cartoon.number_of_series % 10 == 1 and cartoon.number_of_series != 11:
            series_word = "серия"
        elif cartoon.number_of_series % 10 in [2, 3, 4] and cartoon.number_of_series not in [11, 12, 13, 14]:
            series_word = "серии"
        else:
            series_word = "серий"
        
    data = {
        "data": cartoon,
        "seasons_word": seasons_word,
        "series_word": series_word,
        "ml_status": MyListStatus.objects.all(),
        "ml_scores": MyListScores.objects.all(),
        "ml_cartoon_info": ml_cartoon_info
    }

    return render(request, "main/cartoon_page.html", data)

def show_search(request):
    value = request.GET.get('search')   
    
    search_result = Cartoons.objects.filter(Q(eng_title__icontains=value) | Q(rus_title__icontains=value)).order_by('-number_of_ratings')
    data = {
        "search_result": search_result
    }

    return render(request, 'main/search_result.html', data)

@require_POST
def settings(request):
    user_profile = Profile.objects.get(id=request.user.profile.id)
    for key in request.POST:
        setattr(user_profile, key, request.POST[key])
    user_profile.save()
    return HttpResponse('success')

def show_settings(request, username):

    owner = get_object_or_404(User, username=username)
    owner_profile = owner.profile

    if owner.id != request.user.id:
        return redirect('home')
    
    settings = {}
    
    settings["is_list_public"] = owner_profile.is_list_public
    settings["is_cover_in_list"] = owner_profile.is_cover_in_list

    data = {
        'owner_user': owner,
        'owner_profile': owner_profile,
        'settings': json.dumps(settings)
    }
    return render(request, 'main/settings.html', data)

def user_register(request):
    if request.user.is_authenticated:
        messages.error(request, "Вы уже зарегистрированы")
        return redirect('home')
    if request.method == 'POST':
        reg_form = UserRegistrationForm(request.POST)
        if reg_form.is_valid():
            print(reg_form.data)
            print(reg_form.cleaned_data)
            new_user = reg_form.save(commit=False)  
            new_user.set_password(reg_form.cleaned_data['password2'])
            new_user.save()
            login(request, new_user)
            messages.success(request, "Регистрация прошла успешно")
            return redirect('home')
    else:
        reg_form = UserRegistrationForm()
    return render(request, 'main/register.html', {'reg_form': reg_form})

def user_login(request):
    if request.user.is_authenticated:
        messages.error(request, "Вы уже вошли в аккаунт")
        return redirect('home')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, "Добро пожаловать обратно!")
                return redirect('home')
            else:
                return render(request, 'main/login.html', {'log_form': form, "status": "error"})
        return
    form = LoginForm()
    return render(request, 'main/login.html', {'log_form': form, "status": None})


def user_logout(request):
    if request.user.is_authenticated:
        messages.success(request, "Вы вышли из аккаунта")
        logout(request)

    redirect_url = request.META.get('HTTP_REFERER')
    if redirect_url:
        return redirect(redirect_url)
    else:
        return redirect('home')