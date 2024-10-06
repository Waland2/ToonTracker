from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name="home"),
    path('cartoons/', views.show_cartoons, name="cartoons"),
    path('cartoon/<int:cartoon_id>/', views.show_cartoon_page),
    path('cartoon/<int:cartoon_id>/<slug:cartoon_name>/', views.show_cartoon_page),
    path('register/', views.user_register, name="register"),
    path('login/', views.user_login, name="login"),
    path('logout/', views.user_logout, name="logout"),
    path('search/', views.show_search, name="search"),
    path('settings/', views.settings),
    path('settings/<slug:username>/', views.show_settings)
]
