from django import forms
from . import models


class TicketDepartmentForm(forms.ModelForm):
    file = forms.FileField(required=False)

    class Meta:
        model = models.TicketDepartment
        exclude = ('is_open',)
