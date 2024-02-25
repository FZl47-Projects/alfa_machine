from django import forms
from . import models


class PaymentCreate(forms.ModelForm):
    class Meta:
        model = models.Payment
        fields = '__all__'


class PaymentUpdate(PaymentCreate):
    pass


class SuretyBondCreate(forms.ModelForm):

    class Meta:
        model = models.SuretyBond
        fields = '__all__'


class SuretyBondUpdate(SuretyBondCreate):
    pass


class ReminderTimeProjectCreate(forms.ModelForm):
    class Meta:
        model = models.ReminderProject
        fields = '__all__'


class ReminderTimeProjectUpdate(ReminderTimeProjectCreate):
    pass
