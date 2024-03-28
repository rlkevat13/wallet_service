from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.v1.v1_wallet_service.constants import TransactionTypes
from api.v1.v1_wallet_service.models import Wallet, Transaction
from api.v1.v1_wallet_service.serializers import WalletSerializer, TransactionSerializer, DepositWithdrawSerializer, \
    TransactionPaginationSerializer
from utils.custom_serializer_fields import validate_serializers_message


class GetWalletBalanceView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses=WalletSerializer,
        tags=['Wallet Services']
    )
    def get(self, request, version):
        try:
            wallet = Wallet.objects.get(user=request.user)
            if wallet is None:
                return Response({"error": "Wallet not found"}, status=status.HTTP_404_NOT_FOUND)
            response = WalletSerializer(instance=wallet).data
            return Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({'message': ex.args}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DepositToWalletView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=DepositWithdrawSerializer,
        responses=TransactionSerializer,
        tags=['Wallet Services']
    )
    def post(self, request, version):
        try:
            serializer = DepositWithdrawSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({'message': validate_serializers_message(serializer.errors)},
                                status=status.HTTP_400_BAD_REQUEST)
            wallet = Wallet.objects.get(user=request.user)
            if wallet is None:
                return Response({"error": "Wallet not found"}, status=status.HTTP_404_NOT_FOUND)
            wallet.balance += serializer.validated_data.get('amount')
            wallet.save()
            transaction = Transaction.objects.create(wallet=wallet, amount=serializer.validated_data.get('amount'),
                                                     transaction_type=TransactionTypes.deposit)
            response = TransactionSerializer(transaction).data
            return Response(response, status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response({'message': ex.args}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class WithdrawFromWalletView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=DepositWithdrawSerializer,
        responses=TransactionSerializer,
        tags=['Wallet Services']
    )
    def post(self, request, version):
        try:
            serializer = DepositWithdrawSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({'message': validate_serializers_message(serializer.errors)},
                                status=status.HTTP_400_BAD_REQUEST)
            wallet = Wallet.objects.get(user=request.user)
            if wallet is None:
                return Response({"error": "Wallet not found"}, status=status.HTTP_404_NOT_FOUND)
            if wallet.balance < serializer.validated_data.get('amount'):
                return Response({"error": "Insufficient balance"}, status=status.HTTP_400_BAD_REQUEST)
            wallet.balance -= serializer.validated_data.get('amount')
            wallet.save()
            transaction = Transaction.objects.create(wallet=wallet, amount=serializer.validated_data.get('amount'),
                                                     transaction_type=TransactionTypes.withdraw)
            response = TransactionSerializer(transaction).data
            return Response(response, status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response({'message': ex.args}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


#
class GetWalletMiniStatementView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses=TransactionSerializer,
        tags=['Wallet Services']
    )
    def get(self, request, version):
        try:
            wallet = get_object_or_404(Wallet, user=request.user)
            if wallet is None:
                return Response({"error": "Wallet not found"}, status=status.HTTP_404_NOT_FOUND)
            transactions = Transaction.objects.filter(wallet=wallet).order_by('-timestamp')[:10]
            response = TransactionSerializer(transactions, many=True).data
            return Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({'message': ex.args}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ListTransactionHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=TransactionPaginationSerializer,
        responses=TransactionSerializer,
        tags=['Wallet Services']
    )
    def post(self, request, version):
        try:
            serializer = TransactionPaginationSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({'message': validate_serializers_message(serializer.errors)},
                                status=status.HTTP_400_BAD_REQUEST)
            page = self.request.query_params.get('page', 1)
            transactions = Transaction.objects.all().order_by('-timestamp')
            paginator = Paginator(transactions, serializer.validated_data.get('page_count'))
            try:
                transactions_page = paginator.page(page)
            except PageNotAnInteger:
                transactions_page = paginator.page(1)
            except EmptyPage:
                transactions_page = paginator.page(paginator.num_pages)
            response = TransactionSerializer(transactions_page, many=True).data
            return Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({'message': ex.args}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
