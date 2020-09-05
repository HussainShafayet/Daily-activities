from django.urls import path, include
from .import views

urlpatterns = [
    path('', views.main, name='main'),
    path('data/',views.data,name='data'),
    path('add/',views.form,name='add'),
]