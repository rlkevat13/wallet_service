from rest_framework import serializers

from api.v1.v1_wallet_service.constants import TransactionTypes
from api.v1.v1_wallet_service.models import Wallet, Transaction
from utils.custom_serializer_fields import CustomDecimalField, CustomEmailField, CustomIntegerField


class WalletSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, instance: Wallet):
        return instance.user.get_full_name()

    class Meta:
        model = Wallet
        fields = ['id', 'user', 'balance']


class DepositWithdrawSerializer(serializers.Serializer):
    amount = CustomDecimalField(max_digits=10, decimal_places=2)

    @staticmethod
    def validate_amount(value):
        if value < 0:
            raise serializers.ValidationError("Amount cannot be negative")
        if value == 0:
            raise serializers.ValidationError("Amount cannot be zero")
        return value


class TransactionSerializer(serializers.ModelSerializer):
    wallet = serializers.SerializerMethodField()
    transaction_type = serializers.SerializerMethodField()

    def get_wallet(self, instance: Transaction):
        return instance.wallet.balance

    def get_transaction_type(self, instance: Transaction):
        return TransactionTypes.FieldStr.get(instance.transaction_type)

    class Meta:
        model = Transaction
        fields = ['id', 'wallet', 'amount', 'transaction_type', 'timestamp']


class TransactionPaginationSerializer(serializers.Serializer):
    page_count = CustomIntegerField(min_value=0, max_value=100)
