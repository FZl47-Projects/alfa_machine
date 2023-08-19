from django import forms
from . import models


class ItemRegisterForm(forms.ModelForm):
    class Meta:
        model = models.MaterialItem
        exclude = ('is_checked',)


class ItemRegisterUpdateForm(forms.ModelForm):
    class Meta:
        model = models.MaterialItem
        exclude = ('is_checked',)


class ItemsQualityPassForm(forms.ModelForm):
    class Meta:
        model = models.MaterialQuality
        fields = '__all__'
