from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Transaction, Account
from .serializers import TransactionSerializer, AccountSerializer
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.generics import ListCreateAPIView

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

class AccountView(ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class TransactionListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        transactions = Transaction.objects.filter(account__user=request.user)
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)
    @swagger
    def post(self, request):
        serializer = TransactionSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TransactionDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        try:
            return Transaction.objects.get(pk=pk, account__user=user)
        except Transaction.DoesNotExist:
            return None

    def get(self, request, pk):
        transaction = self.get_object(pk, request.user)
        if transaction is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = TransactionSerializer(transaction)
        return Response(serializer.data)
    @swagger
    def patch(self, request, pk):
        transaction = self.get_object(pk, request.user)
        if transaction is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = TransactionSerializer(transaction, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        transaction = self.get_object(pk, request.user)
        if transaction is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        transaction.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)