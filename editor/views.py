from django.shortcuts import redirect, render

from .forms import CartoonForm
from django.contrib import messages
from .models import TempCartoon
from main.models import Cartoons, User, Profile

# Create your views here.
def add_cartoon(request):
    if not request.user.is_authenticated:
        messages.error(request, "Для выполнения этого действия вам нужно войти в свой аккаунт")
        return redirect('home')
    
    user_profile = Profile.objects.get(id=request.user.profile.id)
    if user_profile.is_blocked:
        messages.error(request, "Вам был заблокирован доступ к редактированию")
        return redirect('home')
    

    if request.method == 'POST':
            print(request.FILES)

            form = CartoonForm(request.POST, request.FILES)
            if form.is_valid():
                temp_cartoon = form.save(commit=False)
                temp_cartoon.type_of_request = "add"
                temp_cartoon.user = request.user
                temp_cartoon.save()

                return redirect('home') 
            else:
                return render(request, 'editor/addcartoon.html', {'form': form})
    else:
        form = CartoonForm()

    data = {'form': form}
    return render(request, 'editor/addcartoon.html', data)

def edit_cartoon(request, pk):
    if not request.user.is_authenticated:
        messages.error(request, "Для выполнения этого действия вам нужно войти в свой аккаунт")
        return redirect('home')
    
    user_profile = Profile.objects.get(id=request.user.profile.id)
    if user_profile.is_blocked:
        messages.error(request, "Вам был заблокирован доступ к редактированию")
        return redirect('home')
    

    if request.method == 'POST':
            print(request.FILES)

            form = CartoonForm(request.POST, request.FILES)
            if form.is_valid():
                temp_cartoon = form.save(commit=False)
                temp_cartoon.type_of_request = "edit"
                temp_cartoon.user = request.user
                temp_cartoon.save()

                return redirect('home') 
            else:
                return render(request, 'editor/addcartoon.html', {'form': form})
    else:
        cartoon = Cartoons.objects.get(pk=pk)
        form = CartoonForm(instance=cartoon)

    data = {'form': form}
    return render(request, 'editor/addcartoon.html', data)


from django.http import HttpResponse
def accept_request(request, pk):
    if not request.user.is_superuser:
        redirect('home')
    temp_cartoon = TempCartoon.objects.get(pk=pk)

    fields = [field.name for field in Cartoons._meta.fields if field.name != 'id']
    data = {field: getattr(temp_cartoon, field) for field in fields if hasattr(temp_cartoon, field)}       

    if temp_cartoon.type_of_request == "add":
        new_cartoon = Cartoons(**data)
        new_cartoon.save()

    else:
        cartoon = temp_cartoon.cartoon
        for field in fields:
            val = data[field]
            setattr(cartoon, field, val)
        
        cartoon.save()

    temp_cartoon.delete()

    return redirect('/admin')

def reject_request(request, pk):
    if not request.user.is_superuser:
        redirect('home')
    temp_cartoon = TempCartoon.objects.get(pk=pk)
    temp_cartoon.delete()
    return redirect('/admin')

def ban_user(request, pk):
    if not request.user.is_superuser:
        redirect('home')
    user_profile = Profile.objects.get(user=pk)
    user_profile.is_blocked = True
    user_profile.save()

    TempCartoon.objects.all().filter(user=pk).delete()

    return redirect('/admin')
