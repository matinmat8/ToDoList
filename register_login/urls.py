from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

app_name = 'register_login'

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/Login.html'), name='login'),

    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('reset_password/',
         auth_views.PasswordResetView.as_view(template_name="registration/reset_password.html"),
         name="reset_password"),

    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name="registration/password_reset_done.html"),
         name="password_reset_done"),

    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name="password_reset_confirm"),

    path('reset_password_completed/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_completed"),
    path('email_confirmation/', EmailConfirmation.as_view(), name='email_confirmation'),
    path('email_confirmation/<int:pk>/', AccountActivation.as_view(), name='email_verifying'),
    path('profile/', Profile.as_view(), name='profile'),
]