from django.urls import path
from . import views


app_name = 'notifications'

urlpatterns = [
    path('redirect/<int:pk>/', views.notification_redirect, name='redirect'),
]