from django import forms
from . import models


class WarehouseRegistrationForm(forms.ModelForm):
    class Meta:
        model = models.WarehouseRegistration
        fields = '__all__'
