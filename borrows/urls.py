from django.urls import path
from . import views


app_name = 'borrows'

urlpatterns = [
    path('request/<uuid:copy_id>/', views.request_borrow, name='request-borrow'),
    path('my-loans/', views.my_loans, name='my_loans'),
    path('return/<int:loan_id>/',      views.return_loan,    name='return-loan'),
]

