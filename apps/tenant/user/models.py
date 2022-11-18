from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, name, mobile, password):
        user = self.model(mobile=mobile)
        user.set_password(password)
        user.username = name
        user.save()
        return user

    def create_super_user(self, name, mobile, password):
        user = self.create_user(name=name, mobile=mobile, password=password)
        user.is_superuser = True
        user.save()
        return user


class User(AbstractBaseUser):
    username = models.CharField(max_length=100)
    is_superuser = models.BooleanField(default=False)
    mobile = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username

    objects = UserManager()

    class Meta:
        db_table = 'users'
