from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Transaction, Account
from .serializers import TransactionSerializer, AccountSerializer
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import generics
from rest_framework.viewsets import GenericViewSet,mixins

swagger=swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'amount': openapi.Schema(type=openapi.TYPE_NUMBER, description='Amount'),
                'type': openapi.Schema(type=openapi.TYPE_STRING, description='Type')
            },
            required=['amount','type'],
            example={
                'amount': 100.0,
                'type': 'Cash In'
            }
        ),
        responses={200: 'Success', 400: 'Bad Request'},
    )

class AccountView(mixins.ListModelMixin, mixins.CreateModelMixin,GenericViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class TransactionViewSet(mixins.ListModelMixin,
                         mixins.CreateModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.DestroyModelMixin,
                         GenericViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

   