from django.urls import path, include
from . import views
from django.conf.urls import url

urlpatterns = [
    path('', views.main, name='main'),
    path('about/', views.about, name='about'),
    path('data/', views.data, name='data'),
    path('add/', views.form, name='add'),
    path('show/',views.show_catg,name='show'),
    path('category/',views.add_category,name='category'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit-profile/',views.edit_profile,name='edit-profile'),
    path('profile/change-password/', views.password_change, name='password'),
    path('password_reset/', views.ResetPassword.as_view(), name='password_reset'),
   
    path('password_reset/done/', views.ResetPasswordDone.as_view(), name='password_reset_done'),
     path('password_reset/<uidb64>/<token>/', views.ResetPasswordConfirm.as_view(),
         name='password_reset_confirm'),
    path('reset/done/', views.ResetPasswordComplete.as_view(),
         name='password_reset_complete'),
    path('logout/', views.user_logout, name='logout'),
    path('edit/<int:id>',views.edit,name='edit'),
    path('delete/<int:id>', views.delete, name='delete'),
    path('activate/<uidb64>/<token>/',
        views.activate, name='activate'),

]
