from django import forms
from . import models


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


class TaskStatusCreate(forms.ModelForm):
    file = forms.FileField(required=False)
    description = forms.CharField(required=False)

    class Meta:
        model = models.TaskStatus
        fields = '__all__'


class InquiryAdd(forms.ModelForm):
    class Meta:
        model = models.Inquiry
        fields = '__all__'


class InquiryUpdate(forms.ModelForm):
    class Meta:
        model = models.Inquiry
        exclude = ('from_department',)


class InquiryStatusModify(forms.ModelForm):
    class Meta:
        model = models.InquiryStatus
        fields = '__all__'


class InquiryFile(forms.ModelForm):
    description = forms.CharField(required=False)

    class Meta:
        model = models.InquiryFile
        exclude = ('files',)


class TaskMasterCreate(forms.ModelForm):
    description = forms.CharField(required=False)

    class Meta:
        model = models.TaskMaster
        fields = '__all__'


class TaskMasterUpdate(TaskMasterCreate):
    pass


class DepartmentCreate(forms.ModelForm):
    class Meta:
        model = models.Department
        fields = '__all__'


class DepartmentUpdate(DepartmentCreate):
    pass


class ProjectFileCreate(forms.ModelForm):
    description = forms.CharField(required=False)
    file = forms.FileField(required=True)

    class Meta:
        model = models.ProjectFile
        fields = '__all__'


class ProjectFileUpdate(forms.ModelForm):
    class Meta:
        model = models.ProjectFile
        fields = ('file',)


class ProjectCommentCreate(forms.ModelForm):
    class Meta:
        model = models.ProjectComment
        fields = '__all__'


class ProjectNoteCreate(forms.ModelForm):
    class Meta:
        model = models.ProjectNote
        fields = '__all__'


class ProjectStepCreate(forms.ModelForm):
    description = forms.CharField(required=False)
    actual = forms.IntegerField(required=False)

    class Meta:
        model = models.ProjectStep
        fields = '__all__'


class ProjectStepUpdate(ProjectStepCreate):
    class Meta:
        model = models.ProjectStep
        exclude = ('from_department', 'project')
