from django import forms
from . import models


class PaymentForm(forms.ModelForm):
    class Meta:
        model = models.Payment
        exclude = ('file',)  # TEMP


class PrePaymentForm(forms.ModelForm):
    class Meta:
        model = models.PrePayment
        exclude = ('file',)  # TEMP


class SaveSuretyBondForm(forms.ModelForm):
    class Meta:
        model = models.SuretyBond
        exclude = ('reminder_time',)


class SaveReminderTimeForm(forms.ModelForm):
    class Meta:
        model = models.SuretyBond
        fields = ('project', 'reminder_time',)
