# Generated by Django 5.0.3 on 2024-03-28 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('v1_wallet_service', '0002_alter_transaction_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]