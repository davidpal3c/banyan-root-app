from django.urls import path
from . import views


# app_name = 'userauth'

urlpatterns = [
    path('login_user/', views.login_user, name='login'),
    path('logout_user/', views.logout_user, name='logout'),
    path('register_user/', views.register_user, name='register-user'),
    path('reset_password/', views.reset_password, name='reset-password'),
]

