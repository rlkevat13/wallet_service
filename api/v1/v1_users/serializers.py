from django.utils import timezone
from rest_framework import serializers

from api.v1.v1_users.models import SystemUser
from utils.custom_serializer_fields import CustomCharField, CustomEmailField


class RegisterSerializer(serializers.Serializer):
    email = CustomEmailField()
    first_name = CustomCharField()
    last_name = CustomCharField()
    password = CustomCharField()
    cnf_password = CustomCharField()

    def __init__(self, **kwargs):
        super(RegisterSerializer, self).__init__(**kwargs)

    def validate_email(self, value):
        if SystemUser.objects.filter(username=value).exists():
            raise serializers.ValidationError("A user with this email already exists!")
        return value

    def validate(self, attrs):
        if attrs['password'] != attrs['cnf_password']:
            raise serializers.ValidationError("Passwords do not match!")
        return attrs

    def create(self, validated_data):
        user_obj = SystemUser(username=validated_data.get('email'))
        user_obj.first_name = validated_data.get('first_name')
        user_obj.last_name = validated_data.get('last_name')
        user_obj.updated_at = timezone.now()
        user_obj.set_password(validated_data.get('password'))
        user_obj.save()
        return user_obj


class LoginSerializer(serializers.Serializer):
    email = CustomCharField()
    password = CustomCharField()

    def validate_email(self, value):
        if not SystemUser.objects.filter(username=value).exists():
            raise serializers.ValidationError("A user with this email does not exists!")
        return value


class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemUser
        fields = ['id', 'username', 'first_name', 'last_name']
