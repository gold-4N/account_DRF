from rest_framework import serializers
from .models import Transaction, Account

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields="__all__"


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['amount', 'type']
    
    def validate(self, data):
        user = self.context['request'].user
        account = Account.objects.get(user=user)
        amount = data.get('amount')
        transaction_type = data.get('type')

        if transaction_type == 'Cash Out' and account.amount < amount:
            raise serializers.ValidationError("Insufficient funds for cash out")

        return data

    def create(self, validated_data):
        user = self.context['request'].user
        account = Account.objects.get(user=user)
        transaction_type = validated_data['type']
        amount = validated_data['amount']

        if transaction_type == 'Cash In':
            account.amount += amount
        elif transaction_type == 'Cash Out':
            account.amount -= amount

        account.save()
        return Transaction.objects.create(account=account, **validated_data)

    def update(self, instance, validated_data):
        user = self.context['request'].user
        account = Account.objects.get(user=user)
        old_amount = instance.amount
        old_type = instance.type
        new_amount = validated_data.get('amount', old_amount)
        new_type = validated_data.get('type', old_type)

        if old_type == 'Cash In':
            account.amount -= old_amount
        elif old_type == 'Cash Out':
            account.amount += old_amount

        if new_type == 'Cash In':
            account.amount += new_amount
        elif new_type == 'Cash Out':
            if account.amount < new_amount:
                raise serializers.ValidationError("Insufficient funds for cash out")
            account.amount -= new_amount

        account.save()
        instance.amount = new_amount
        instance.type = new_type
        instance.save()
        return instance
