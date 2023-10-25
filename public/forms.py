from django import forms
from . import models


class TaskCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TaskCreateForm, self).__init__(*args, **kwargs)
        for field_name, field_inp in self.fields.items():
            if field_name not in self.Meta.required:
                field_inp.required = False

    class Meta:
        model = models.Task
        exclude = ('is_active',)
        required = ('name', 'project', 'to_department', 'from_department')


class TaskUpdateForm(TaskCreateForm, forms.ModelForm):
    file = forms.FileField(required=False)

    class Meta:
        model = models.Task
        exclude = ('is_active', 'allocator_user', 'from_department', 'state')
        required = ('name', 'project', 'to_department', 'from_department')


class TaskStateUpdate(forms.Form):
    state = forms.ChoiceField(choices=models.Task.STATE_OPTIONS)


class ProjectFile(forms.ModelForm):
    file = forms.FileField(required=True)

    class Meta:
        model = models.ProjectFile
        fields = '__all__'


class ProjectAdd(forms.ModelForm):
    item = forms.CharField(required=False)
    description = forms.CharField(required=False)

    class Meta:
        model = models.Project
        exclude = ('is_active',)


class ProjectUpdate(forms.ModelForm):
    item = forms.CharField(required=False)
    description = forms.CharField(required=False)

    class Meta:
        model = models.Project
        exclude = ('is_active',)


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


class InquiryFileForm(forms.ModelForm):

    class Meta:
        model = models.InquiryFile
        fields = '__all__'

