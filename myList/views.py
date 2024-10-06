from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from .models import *
from main.models import Cartoons
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.db.models import Q

@require_POST
def cartoon_list(request):
    post_queries = request.POST
    ml_object = MyListObject.objects.filter(user__id=post_queries.get('user_id'), cartoon__id=post_queries['cartoon_id'])
    if ml_object and post_queries.get("delete"):
        ml_object[0].delete()

    cartoon = Cartoons.objects.get(id=post_queries['cartoon_id'])
    user = User.objects.get(id=post_queries['user_id'])
    watch_status = MyListStatus.objects.get(id=post_queries['status'])

    if post_queries.get('score') != 'null':
        score = MyListScores.objects.get(id=post_queries['score'])
    else:
        score = None
    
    comment = post_queries['comment']
    
    if ml_object:

        ml_object.update(
            cartoon=cartoon,
            user=user,
            watch_status=watch_status,
            score=score,
            comment=comment
        )

    else:
        new_object = MyListObject(
            cartoon=cartoon,
            user=user,
            watch_status=watch_status,
            score=score,
            comment=comment
        ) 

        new_object.save()
    return HttpResponse("done")


# Create your views here.
def show_user_cartoon_list(request, username):
    if not request.user.is_authenticated:
        messages.error(request, "Для выполнения этого действия вам нужно войти в свой аккаунт")
        return redirect('home')
    
    owner = get_object_or_404(User, username=username)
    owner_list = MyListObject.objects.filter(user__username=username).order_by("watch_status__priority_in_list", "cartoon__rus_title")

    is_status = request.GET.get('status')
    if is_status and is_status != "0":
        owner_list = owner_list.filter(watch_status__id=is_status)

    is_sort = request.GET.get('sort')
    static_sort = is_sort
    if is_sort:
        if is_sort.find('-') != -1:
            is_sort = is_sort.replace('-', '')
        else:
            is_sort = '-' + is_sort
        if is_sort.find('cartoon') != -1: is_sort += '__rus_title'
        owner_list = owner_list.order_by(is_sort)

    data = {
        'owner': owner.profile,
        'owner_user': owner,
        'owner_list': owner_list,
        'watch_status': is_status,
        'sort_type': static_sort 
    }
    return render(request, "myList/cartoonlist.html", data)