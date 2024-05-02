from django.urls import path
from django.contrib.auth import views as auth_views

from . import views


app_name = 'users'
urlpatterns = [
    # path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),

    path('login/', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
]
