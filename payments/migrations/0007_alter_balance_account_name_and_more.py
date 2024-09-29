# Generated by Django 5.0.7 on 2024-09-27 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0006_balance_created_on'),
    ]

    operations = [
        migrations.AlterField(
            model_name='balance',
            name='account_name',
            field=models.CharField(default='', max_length=444),
        ),
        migrations.AlterField(
            model_name='balance',
            name='account_number',
            field=models.CharField(default='', max_length=202),
        ),
        migrations.AlterField(
            model_name='balance',
            name='amount_withdraw',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='balance',
            name='bank_code',
            field=models.CharField(default='', max_length=202),
        ),
        migrations.AlterField(
            model_name='balance',
            name='bank_name',
            field=models.CharField(default='', max_length=200),
        ),
    ]
