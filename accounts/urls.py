# accounts/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import RegisterView, ProfileView

app_name = 'accounts'

urlpatterns = [
    # login / logout still use Django's built-ins
    path(
        'login/',
        auth_views.LoginView.as_view(template_name='accounts/login.html'),
        name='login'
    ),
    path(
        'logout/',
        auth_views.LogoutView.as_view(),
        name='logout'
    ),

    # class-based registration
    path(
        'register/',
        RegisterView.as_view(),
        name='register'
    ),

    # class-based profile (LoginRequiredMixin)
    path(
        'profile/',
        ProfileView.as_view(),
        name='profile'
    ),
]
