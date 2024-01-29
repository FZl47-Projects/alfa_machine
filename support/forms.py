from django import forms
from . import models


class TicketDepartmentCreate(forms.ModelForm):
    description = forms.CharField(required=False)
    file = forms.FileField(required=False)

    class Meta:
        model = models.TicketDepartment
        exclude = ('is_open', 'number_id', 'projects', 'projects_type')

