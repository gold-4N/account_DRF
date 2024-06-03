from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from .models import Account, Transaction
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
# Create your views here.




class AccountView(APIView):

    def get(self, request):
        account=Account.objects.all()
        
        serializer=AccountSerializer(account,many=True)
        return Response(serializer.data)
    

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT
        ),
        responses={200: 'Success', 400: 'Bad Request'},
    )
    def post(self,request):
        serializer=AccountSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class TransactionView(APIView):
    def get(self,request):
        transaction=Transaction.objects.all()
        serializer=AllTransactionSerializer(transaction,many=True)
        return Response(serializer.data)

class CashinView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        chackin=Transaction.objects.filter(account__user=request.user,type ='Cash In')
        serializer=TransactionSerializer(chackin,many=True)
        return Response(serializer.data)
    
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'amount': openapi.Schema(type=openapi.TYPE_NUMBER, description='Amount to cash in')
            },
            required=['amount'],
            example={
                'amount': 100.0
            }
        ),
        responses={200: 'Success', 400: 'Bad Request'},
    )
    def post(self,request):
        serializer=TransactionSerializer(data=request.data)
        if serializer.is_valid():
            account=Account.objects.get(user=request.user)
            cash_in=Transaction.objects.create(type='Cash In',amount=serializer.validated_data['amount'],account=account)
            cash_in.save()
            account.amount+=cash_in.amount 
            account.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CashoutView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        chackin=Transaction.objects.filter(account__user=request.user,type ='Cash Out')
        serializer=TransactionSerializer(chackin, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'amount': openapi.Schema(type=openapi.TYPE_NUMBER, description='Amount to cash out')
            },
            required=['amount'],
            example={
                'amount': 100.0
            }
        ),
        responses={200: 'Success', 400: 'Bad Request'},
    )
    def post(self,request):
        serializer=TransactionSerializer(data=request.data)
        if serializer.is_valid():
            account=Account.objects.get(user=request.user)
            if account.amount-serializer.validated_data['amount']>=0:
                cash_in=Transaction.objects.create(type='Cash Out',amount=float(serializer.validated_data['amount']),account=account)
                cash_in.save()
                account.amount-=cash_in.amount 
                account.save()
                
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                Response({'massage':"not sufficient balance to cash out"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)