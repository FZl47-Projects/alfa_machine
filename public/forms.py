from django import forms
from . import models


class TaskCreate(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TaskCreate, self).__init__(*args, **kwargs)
        for field_name, field_inp in self.fields.items():
            if field_name not in self.Meta.required:
                field_inp.required = False

    class Meta:
        model = models.Task
        exclude = ('is_active',)
        required = ('name', 'project', 'to_department', 'from_department')


class TaskUpdate(TaskCreate, forms.ModelForm):
    file = forms.FileField(required=False)

    class Meta:
        model = models.Task
        exclude = ('is_active', 'allocator_user', 'to_department', 'from_department', 'project')
        required = ('name',)


# TaskMasterAdd form
class TaskMasterAddForm(forms.ModelForm):
    class Meta:
        model = models.TaskMaster
        fields = '__all__'


class ProjectFile(forms.ModelForm):
    file = forms.FileField(required=True)

    class Meta:
        model = models.ProjectFile
        fields = '__all__'


class ProjectCreate(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ProjectCreate, self).__init__(*args, **kwargs)
        for field_name, field_inp in self.fields.items():
            if field_name in self.Meta.not_required:
                field_inp.required = False

    item = forms.CharField(required=False)
    description = forms.CharField(required=False)

    class Meta:
        model = models.Project
        exclude = ('is_active',)
        not_required = ('inquiry',)


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
