from django.test import TestCase

from django.urls import path
from .views import request_borrow, my_loans

app_name = 'borrows'

urlpatterns = [
    path('request/<uuid:copy_id>/', request_borrow, name='request-borrow'),
    path('my-loans/', my_loans, name='my_loans'),
]