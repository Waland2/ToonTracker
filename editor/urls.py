from django.urls import path, include
from . import views

urlpatterns = [
    path('addcartoon/', views.add_cartoon, name="addcartoon"),
    path('edit/<int:pk>', views.edit_cartoon, name="editcartoon"),    
    path('acceptrequest/<int:pk>/', views.accept_request, name='acceptrequest'),
    path('rejectrequest/<int:pk>/', views.reject_request, name='rejectrequest'),
    path('blockuser/<int:pk>', views.ban_user, name='blockuser')
]
