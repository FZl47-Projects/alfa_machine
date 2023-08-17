from django.db import models
from core.models import BaseModel, File


class BasePayment(BaseModel, File):
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
