from django.contrib import admin
from django.urls import path,include
from .views import *



urlpatterns = [
      path('account/',AccountView.as_view(),name='account'),
      path('all-transactinos/',TransactionView.as_view(),name='all-transactinos'),
      path('cash-in/',CashinView.as_view(),name='cash-in'),
      path('cash-out/',CashoutView.as_view(),name='cash-out'),
]
