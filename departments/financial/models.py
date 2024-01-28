from django.db import models
from core.models import BaseModel, FileAbstract


class BasePayment(BaseModel, FileAbstract):
    TYPE_PAYMENT_OPTIONS = (
        ('deposit', 'واریزی'),
        ('payment', 'پرداختی'),
    )
    type_payment = models.CharField(max_length=20, choices=TYPE_PAYMENT_OPTIONS)
    price = models.BigIntegerField()
    tracking_code = models.CharField(max_length=100)
    project = models.ForeignKey('public.Project', on_delete=models.CASCADE)
    submited_at = models.DateField()

    class Meta:
        ordering = '-id',
        abstract = True

    def __str__(self):
        return f'payment {self.project}'

    def get_type_payment_label(self):
        return self.get_type_payment_display()


class Payment(BasePayment):
    pass


class PrePayment(BasePayment):
    pass


# SuretyBond model
class SuretyBond(BaseModel, FileAbstract):
    project = models.OneToOneField('public.Project', on_delete=models.CASCADE, related_name='surety_bond')
    number_id = models.CharField(max_length=32, null=True, blank=True)
    is_free = models.BooleanField(default=False)
    reminder_time = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return f'{self.project.name}: {self.number_id}'

    def get_reminder_time(self):
        if self.reminder_time:
            return self.reminder_time.strftime('%Y-%m-%d')
