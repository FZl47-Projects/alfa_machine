from django import forms
from . import models


class NotificationDepartmentCreate(forms.ModelForm):
    description = forms.CharField(required=False)
    file = forms.FileField(required=False)

    class Meta:
        model = models.NotificationDepartment
        exclude = ('projects', 'projects_type')


class NotificationDepartmentUpdate(NotificationDepartmentCreate):
    class Meta:
        model = models.NotificationDepartment
        exclude = ('projects', 'projects_type', 'from_department', 'to_departments')
