from django import forms
from . import models


class ItemWarehouseCreate(forms.ModelForm):
    class Meta:
        model = models.ItemWarehouse
        fields = '__all__'


class ItemWarehouseUpdate(ItemWarehouseCreate):
    pass


class ItemWarehouseFileCreate(forms.ModelForm):
    class Meta:
        model = models.ItemFile
        fields = '__all__'
