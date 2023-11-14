from django import forms
from . import models


class TicketDepartmentForm(forms.ModelForm):
    file = forms.FileField(required=False)

    class Meta:
        model = models.TicketDepartment
        exclude = ('is_open',)

    def clean_is_all_projects(self):
        cleaned_data = self.clean()

        project_selection = self.data.get('project_selection')
        is_all_projects = cleaned_data.get('is_all_projects')
        projects = cleaned_data.get('projects')

        if project_selection == 'null':
            pass
        elif is_all_projects is False and not projects:
            self.add_error('projects', 'please enter project object')

        return is_all_projects

    def clean_is_all_departments(self):
        cleaned_data = self.clean()

        is_all_departments = cleaned_data.get('is_all_departments')
        departments = cleaned_data.get('departments')

        if is_all_departments is False and not departments:
            self.add_error('departments', 'please enter department object')

        return is_all_departments


class ReportDepartmentForm(forms.ModelForm):
    file = forms.FileField(required=False)

    class Meta:
        model = models.Report
        fields = '__all__'

    def clean_is_all_projects(self):
        cleaned_data = self.clean()

        project_selection = self.data.get('project_selection')
        is_all_projects = cleaned_data.get('is_all_projects')
        projects = cleaned_data.get('projects')

        if project_selection == 'null':
            pass
        elif is_all_projects is False and not projects:
            self.add_error('projects', 'please enter project object')

        return is_all_projects

    def clean_is_all_departments(self):
        cleaned_data = self.clean()

        is_all_departments = cleaned_data.get('is_all_departments')
        departments = cleaned_data.get('departments')

        if is_all_departments is False and not departments:
            self.add_error('departments', 'please enter department object')

        return is_all_departments
