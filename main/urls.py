from django.urls import path, include
from .import views

urlpatterns = [
    path('', views.main, name='main'),
    path('data/',views.data,name='data'),
    path('add/', views.form, name='add'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout, name='logout'),
]
