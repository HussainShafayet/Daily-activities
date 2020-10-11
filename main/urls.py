from django.urls import path, include
from .import views

urlpatterns = [
    path('', views.main, name='main'),
    path('about/', views.about, name='about'),
    path('data/', views.data, name='data'),
    path('add/', views.form, name='add'),
    path('show/',views.show_catg,name='show'),
    path('category/',views.add_category,name='category'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('profile/',views.profile,name='profile'),
    path('logout/', views.logout, name='logout'),
    path('edit/<int:id>',views.edit,name='edit'),
    path('delete/<int:id>', views.delete, name='delete'),

]
