from django import forms
from . import models


class NotificationDepartmentForm(forms.ModelForm):
    class Meta:
        model = models.NotificationDepartment
        exclude = ('is_showing',)

    def clean_is_all_projects(self):
        cleaned_data = self.clean()
        is_all_projects = cleaned_data.get('is_all_projects')
        projects = cleaned_data.get('projects')
        if is_all_projects is False and not projects:
            self.add_error('projects', 'please enter project object')
        return is_all_projects

    def clean_is_all_departments(self):
        cleaned_data = self.clean()
        is_all_departments = cleaned_data.get('is_all_departments')
        departments = cleaned_data.get('departments')
        if is_all_departments is False and not departments:
            self.add_error('departments', 'please enter department object')
        return is_all_departments
