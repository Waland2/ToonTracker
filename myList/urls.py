from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.cartoon_list, name='cartoonlist'),
    path('<slug:username>/', views.show_user_cartoon_list, name="usercartoonlist")
]
