from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.v1.v1_users.models import SystemUser
from api.v1.v1_users.serializers import RegisterSerializer, LoginSerializer, UserDetailsSerializer
from api.v1.v1_wallet_service.models import Wallet
from utils.custom_serializer_fields import validate_serializers_message


class RegisterView(APIView):
    @extend_schema(
        request=RegisterSerializer,
        responses={200: "application/json"},
        tags=['Users']
    )
    def post(self, request, version):
        try:
            serializer = RegisterSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({'message': validate_serializers_message(serializer.errors)},
                                status=status.HTTP_400_BAD_REQUEST)
            user_obj = serializer.save()
            Wallet.objects.create(user=user_obj, balance=0.0)
            return Response({'message': 'User registered successfully.'}, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({'message': ex.args}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoginView(APIView):
    @extend_schema(
        request=LoginSerializer,
        responses=UserDetailsSerializer,
        tags=['Users']
    )
    def post(self, request, version):
        try:
            serializer = LoginSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({'message': validate_serializers_message(serializer.errors)},
                                status=status.HTTP_400_BAD_REQUEST)
            sys_obj: SystemUser = SystemUser.objects.filter(username=serializer.validated_data.get('email'))
            if not sys_obj.exists():
                return Response({'message': 'Invalid Credentials.'}, status=status.HTTP_400_BAD_REQUEST)
            sys_obj = sys_obj.first()
            if not sys_obj.check_password(serializer.validated_data.get('password')):
                return Response({'message': 'Incorrect Password.'}, status=status.HTTP_400_BAD_REQUEST)
            response_data = UserDetailsSerializer(instance=sys_obj).data
            token = Token.objects.get_or_create(user=sys_obj)[0]
            response_data['token'] = token.key
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({'message': ex.args}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserListView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses=UserDetailsSerializer,
        tags=['Users']
    )
    def get(self, request, version):
        try:
            user_obj: SystemUser = SystemUser.objects.filter(username=request.user)
            user_obj = user_obj.first()
            if not user_obj.is_superuser:
                return Response({'message': 'Sorry! You do not have permission.'}, status=status.HTTP_403_FORBIDDEN)
            response = UserDetailsSerializer(
                instance=SystemUser.objects.filter(is_superuser=False).order_by('-id'), many=True).data
            return Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({'message': ex.args}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
