from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core import signing
from django.db import models

from utils.custom_manager import UserManager


class SystemUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=254, unique=True)
    first_name = models.CharField(max_length=50, null=True, blank=True, default=None)
    last_name = models.CharField(max_length=50, null=True, blank=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True, default=None)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def get_signing_dumps(self):
        return signing.dumps(self.pk)

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        db_table = "system_user"
