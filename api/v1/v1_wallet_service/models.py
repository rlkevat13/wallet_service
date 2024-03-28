from django.core import signing
from django.db import models

from api.v1.v1_users.models import SystemUser
from api.v1.v1_wallet_service.constants import TransactionTypes


# Create your models here.
class Wallet(models.Model):
    user = models.OneToOneField(SystemUser, on_delete=models.CASCADE, related_name='user_wallet')
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def get_signing_dumps(self):
        return signing.dumps(self.pk)

    def __str__(self):
        return f"Wallet of {self.user.username}"

    class Meta:
        db_table = "wallet"


class Transaction(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name="wallet_transactions")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.IntegerField(null=True, choices=TransactionTypes.FieldStr.items(), default=None)
    timestamp = models.DateTimeField(auto_now_add=True)

    def get_signing_dumps(self):
        return signing.dumps(self.pk)

    def __str__(self):
        return f"{TransactionTypes.FieldStr.get(self.transaction_type).capitalize()} of {self.amount} on {self.timestamp}"

    def get_transaction_type(self):
        return TransactionTypes.FieldStr.get(self.transaction_type)

    class Meta:
        db_table = "transaction"
