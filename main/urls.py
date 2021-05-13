from django.urls import path, include
from . import views
from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.main, name='main'),
    path('about/', views.about, name='about'),
    path('data/<str:title_name>/', views.data, name='data'),
    path('pdf/<str:title_name>/', views.GeneratePdf, name='pdf'),
    path('inactive/<str:title_name>',views.expenses_active,name='inactive'),
    path('archive_expenses/', views.archive_expenses, name='archive'),
    path('new_expenses_record/', views.add_expenses_tilte, name='new_record'),
    path('all_expenses/', views.show_expenses_title, name='show_expenses_title'),
    path('show_expenses/', views.show_expenses_title2, name='show_expenses_title2'),
    path('add/<str:title_name>', views.form, name='add'),
    path('show/', views.show_catg, name='show'),
    path('search_item/', csrf_exempt(views.search_item), name='search'),
    path('category/<str:title_name>/',views.add_category,name='category'),
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
    path('edit/<str:title_name>/<int:id>',views.edit,name='edit'),
    path('delete/<str:title_name>/<int:id>', views.delete, name='delete'),
    path('activate/<uidb64>/<token>/',
        views.activate, name='activate'),

]
