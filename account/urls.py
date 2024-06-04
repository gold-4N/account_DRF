from django.contrib import admin
from django.urls import path,include
from .views import *



urlpatterns = [
            path('transactions/', TransactionListCreateAPIView.as_view(), name='transaction-list-create'),
            path('account/',AccountView.as_view(),name='account'),
            path('transactions/<int:pk>/', TransactionDetailAPIView.as_view(), name='transaction-detail'),
  
]
