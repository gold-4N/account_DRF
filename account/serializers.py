from rest_framework import serializers
from .models import *

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields="__all__"

class AllTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Transaction
        fields="__all__"

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Transaction
        fields=['amount']