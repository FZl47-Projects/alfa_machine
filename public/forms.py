from django import forms
from . import models


class TaskCreateForm(forms.ModelForm):
    file = forms.FileField(required=False)

    class Meta:
        model = models.Task
        exclude = ('is_active',)


class TaskUpdateForm(forms.ModelForm):
    file = forms.FileField(required=False)

    class Meta:
        model = models.Task
        exclude = ('is_active', 'allocator_user', 'from_department', 'state')
