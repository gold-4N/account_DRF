from django.contrib import admin
from django.urls import path,include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'transactions', TransactionViewSet, basename='transaction-list-create')
# router.register(r'transactions/<int:pk>', TransactionViewSet, basename='transaction-detail')
router.register(r'account',AccountView,basename='account')


urlpatterns = [
           path('',include(router.urls)),
  
]
