from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Account(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    amount=models.FloatField(default=0)
    date=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'account of {self.user.username}'

class Transaction(models.Model):
    TYPE=(
        ('Cash In','Cash In'),
        ('Cash Out','Cash Out') 

    )
    account=models.ForeignKey(Account, on_delete=models.CASCADE)
    type=models.CharField(max_length=50,choices=TYPE)
    amount=models.FloatField()
    date=models.DateTimeField(auto_now_add=True)
    
    # def save(self, *args, **kwargs):
    #     # Update account balance based on transaction type
    #     if self.type == 'Cash In':
    #         self.account.amount += self.amount
    #     elif self.type == 'Cash Out':
    #         self.account.amount -= self.amount
    #     self.account.save()
    #     super().save(*args, **kwargs)
    