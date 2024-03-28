from django.urls import re_path

from api.v1.v1_wallet_service.views import GetWalletBalanceView, DepositToWalletView, WithdrawFromWalletView, \
    GetWalletMiniStatementView, ListTransactionHistoryView

urlpatterns = [
    re_path(r'^(?P<version>(v1))/wallet/balance/', GetWalletBalanceView.as_view()),
    re_path(r'^(?P<version>(v1))/wallet/deposit/', DepositToWalletView.as_view()),
    re_path(r'^(?P<version>(v1))/wallet/withdraw/', WithdrawFromWalletView.as_view()),
    re_path(r'^(?P<version>(v1))/wallet/mini/statement/', GetWalletMiniStatementView.as_view()),
    re_path(r'^(?P<version>(v1))/wallet/transaction/history/list/', ListTransactionHistoryView.as_view()),
]
