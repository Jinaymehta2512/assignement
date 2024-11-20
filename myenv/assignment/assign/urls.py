from django.urls import path
from .views import *

urlpatterns = [
    path('transactions/', TransactionCreateView.as_view(), name='transaction_create'),
    path('transactions/user/', TransactionListView.as_view(), name='transaction_list'),
    path('transactions/<int:pk>/', TransactionDetailView.as_view(), name='transaction_detail'),
]
