from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
class ScrumUserManager(BaseUserManager):
    def create_user(self, username, password=None):

        if username is None:
            raise TypeError('Users must have a username.')

        # if email is None:
        #     raise TypeError('Users must have an email address.')

        user = self.model(username=username)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, password):
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(username, password)
        user.user_type = 'O'
        user.is_superuser = True
        user.is_staff = True
        user.is_admin = True
        user.save()

        return user

class Company(models.Model):
    name = models.CharField(max_length=150, default='linuxjobber')

    def __str__(self):
        return self.name

class ScrumUser(AbstractBaseUser, PermissionsMixin):
    USERTYPE = (('O', 'Owner'), ('U', 'User'))
    # DEFAULT_COMPANY = 1

    username = models.CharField(db_index=True, max_length=255, unique=True)
    full_name = models.CharField(max_length=150)
    user_type = models.CharField(choices=USERTYPE, max_length=1)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    # company = models.ForeignKey(Company, on_delete=models.PROTECT, default=DEFAULT_COMPANY)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = ScrumUserManager()

    def __str__(self):
        return self.username