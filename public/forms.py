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


class TaskStateUpdate(forms.Form):
    state = forms.ChoiceField(choices=models.Task.STATE_OPTIONS)


class ProjectFile(forms.ModelForm):
    file = forms.FileField(required=True)

    class Meta:
        model = models.ProjectFile
        fields = '__all__'


class InquiryForm(forms.ModelForm):
    class Meta:
        model = models.Inquiry
        fields = '__all__'


class InquiryUpdateForm(forms.ModelForm):
    class Meta:
        model = models.Inquiry
        exclude = ('from_department',)


class InquiryStatusForm(forms.ModelForm):

    class Meta:
        model = models.InquiryStatus
        fields = '__all__'
