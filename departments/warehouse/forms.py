from django import forms
from . import models


class WarehouseRegistrationForm(forms.ModelForm):
    class Meta:
        model = models.WarehouseRegistration
        fields = '__all__'


class RegistrationFileForm(forms.ModelForm):
    class Meta:
        model = models.RegistrationFile
        fields = '__all__'
