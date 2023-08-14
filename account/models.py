from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser


class CustomBaseUserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(password=password, role='super_user', email=email,
                                **extra_fields)


class User(AbstractUser):
    ROLE_USER_OPTIONS = (
        ('super_user', 'super_user'),
        ('control_project_user', 'control_project_user'),
        ('control_quality_user', 'quality_control_user'),
        ('commerce_user', 'commerce_user'),
        ('financial_user', 'financial_user'),
        ('warehouse_user', 'warehouse_user'),
        ('production_user', 'production_user'),
        ('technical_user', 'technical_user'),
    )

    first_name = models.CharField("first name", max_length=150, blank=True, default="بدون نام")
    username = None
    email = models.EmailField("email address", null=True, blank=True, unique=True)

    # type users|roles
    role = models.CharField(max_length=20, choices=ROLE_USER_OPTIONS)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomBaseUserManager()

    class Meta:
        ordering = '-id',

    def __str__(self):
        return f'{self.role} - {self.email}'

    def get_full_name(self):
        fl = f'{self.first_name} {self.last_name}'.strip() or 'بدون نام'
        return fl

    def get_email(self):
        return self.email

    def get_last_login(self):
        if self.last_login:
            return self.last_login.strftime('%Y-%m-%d %H:%M:%S')
        return '-'
