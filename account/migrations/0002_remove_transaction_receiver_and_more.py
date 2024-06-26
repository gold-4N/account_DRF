# Generated by Django 5.0.6 on 2024-06-03 06:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='receiver',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='sender',
        ),
        migrations.AddField(
            model_name='transaction',
            name='account',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='account.account'),
            preserve_default=False,
        ),
    ]
