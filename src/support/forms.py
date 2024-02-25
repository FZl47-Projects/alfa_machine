from django import forms
from . import models


class TicketDepartmentCreate(forms.ModelForm):
    description = forms.CharField(required=False)
    file = forms.FileField(required=False)

    class Meta:
        model = models.TicketDepartment
        exclude = ('is_open', 'number_id', 'projects', 'projects_type')


class TicketDepartmentUpdate(forms.ModelForm):
    description = forms.CharField(required=False)
    file = forms.FileField(required=False)

    class Meta:
        model = models.TicketDepartment
        exclude = ('projects', 'projects_type', 'to_departments', 'from_department')
