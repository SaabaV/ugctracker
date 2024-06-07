from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission, UserManager


class CustomUserManager(UserManager):
    def normalize_email(self, email):
        return email.lower()

    def active_users(self):
        return self.filter(is_active=True)

    def get_admins(self):
        return self.filter(is_staff=True, is_superuser=True)


class User(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    groups = models.ManyToManyField(Group, verbose_name='groups', blank=True, related_name='custom_user_groups')
    user_permissions = models.ManyToManyField(Permission, verbose_name='user permissions', blank=True, related_name='custom_user_permissions')

