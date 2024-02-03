from django.db import models
from django.urls import reverse
from core.models import BaseModel, FileAbstract


class Payment(BaseModel, FileAbstract):
    TYPE_PAYMENT_OPTIONS = (
        ('prepayment', 'پیش پرداخت'),
        ('payment', 'پرداخت'),
    )

    TYPE_STATUS_PAYMENT_OPTIONS = (
        ('deposit', 'واریزی'),
        ('payment', 'پرداختی'),
    )

    tracking_code = models.CharField(max_length=100)
    type_payment = models.CharField(max_length=20, choices=TYPE_PAYMENT_OPTIONS)
    type_status_payment = models.CharField(max_length=20, choices=TYPE_STATUS_PAYMENT_OPTIONS)
    price = models.BigIntegerField()
    project = models.ForeignKey('public.Project', on_delete=models.CASCADE)
    submited_at = models.DateField()
    description = models.TextField(null=True, blank=True)

    class Meta:
        ordering = '-id',

    def __str__(self):
        return f'payment {self.project}'

    @classmethod
    def has_perm_to_modify(cls, user):
        if user.is_anonymous:
            return False
        if user.role in ('financial_user', 'super_user'):
            return True
        return False

    def get_absolute_url(self):
        return reverse('dp_financial:payment__detail', args=(self.id,))

    def get_type_payment_label(self):
        return self.get_type_payment_display()

    def get_type_status_payment_label(self):
        return self.get_type_status_payment_display()


class SuretyBond(BaseModel, FileAbstract):
    STATUS_OPTIONS = (
        ('free', 'ازاد'),
        ('restricted', 'قفل'),
    )
    project = models.OneToOneField('public.Project', on_delete=models.CASCADE)
    number_id = models.CharField(max_length=40, null=True, blank=True)
    status = models.CharField(max_length=12, choices=STATUS_OPTIONS)
    description = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return f'{self.project.name}: {self.number_id}'

    @classmethod
    def has_perm_to_modify(cls, user):
        if user.is_anonymous:
            return False
        if user.role in ('financial_user', 'super_user'):
            return True
        return False

    def get_absolute_url(self):
        return reverse('dp_financial:surety_bond__detail', args=(self.id,))

    def get_status_label(self):
        return self.get_status_display()


class ReminderProject(BaseModel):
    project = models.OneToOneField('public.Project', on_delete=models.CASCADE)
    time = models.DateField()
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'reminder - {self.project.name}'

    @classmethod
    def has_perm_to_modify(cls, user):
        if user.is_anonymous:
            return False
        if user.role in ('financial_user', 'super_user'):
            return True
        return False

    def get_remaining_time(self):
        return self.get_remaining_date_field(self.time)
