from django.shortcuts import Http404
from django.urls import reverse_lazy, reverse
from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from core.models import BaseModel
from support.models import TicketDepartment


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


class User(AbstractUser, BaseModel):
    ROLE_USER_OPTIONS = (
        ('super_user', 'کاربر مدیر'),
        ('control_project_user', 'کاربر کنترل پروژه'),
        ('control_quality_user', 'کاربر کنترل کیفی'),
        ('commerce_user', 'کاربر بازرگانی'),
        ('procurement_commerce_user', 'کاربر بازرگانی-فروش'),
        ('financial_user', 'کاربر مالی'),
        ('warehouse_user', 'کاربر انبار'),
        ('production_user', 'کابر تولید'),
        ('technical_user', 'کاربر فنی'),
    )

    first_name = models.CharField("first name", max_length=150, blank=True, default="بدون نام")
    username = None
    email = models.EmailField("email address", null=True, blank=True, unique=True)
    department = models.ForeignKey('public.Department', on_delete=models.SET_NULL, null=True)
    # type users|roles
    role = models.CharField(max_length=32, choices=ROLE_USER_OPTIONS)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomBaseUserManager()

    class Meta:
        ordering = '-id',

    def __str__(self):
        return f'{self.role} - {self.email}'

    @classmethod
    def has_perm_to_modify(cls, user):
        if user.is_anonymous:
            return False
        if user.role in ('super_user',):
            return True
        return False

    def get_role_label(self):
        return self.get_role_display()

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'.strip() or 'بدون نام'

    def get_email(self):
        return self.email

    def get_last_login(self):
        if self.last_login:
            return self.last_login.strftime('%Y-%m-%d %H:%M:%S')
        return '-'

    def get_tickets(self):
        return self.department.to_deps_ticket.filter(is_open=True)

    def get_reports(self):
        return self.department.report_set.all()

    def has_new_ticket(self):
        if self.get_unseen_tickets():
            return True
        return False

    def has_new_notification(self):
        if self.get_unseen_notifications():
            return True
        return False

    def get_unseen_tickets(self):
        unseen = self.department.get_tickets().filter(seen=False)
        return unseen

    def get_unseen_notifications(self):
        unseen = self.department.get_notifications().filter(seen=False)
        return unseen

    def get_absolute_url_dashboard(self):
        user_dashboards = {
            'super_user': reverse_lazy('dp_general:index'),
            'control_project_user': reverse_lazy('dp_control_project:index'),
            'control_quality_user': reverse_lazy('dp_control_quality:index'),
            'commerce_user': reverse_lazy('dp_commerce:index'),
            'procurement_commerce_user': reverse_lazy('dp_commerce:procurement_index'),
            'financial_user': reverse_lazy('dp_financial:index'),
            'warehouse_user': reverse_lazy('dp_warehouse:index'),
            'production_user': reverse_lazy('dp_production:index'),
            'technical_user': reverse_lazy('dp_technical:index'),
        }
        role = self.role
        try:
            return user_dashboards[role]
        except KeyError:
            raise Http404

    def get_absolute_url(self):
        return reverse('account:user__detail', args=(self.id,))

    def get_picture_url(self):
        return '/static/frontend/images/public/default-user.png'
