from django.db import models
from core.utils import get_time, get_timesince_persian, random_str


def upload_file_src(instance, path):
    frmt = str(path).split('.')[-1]
    tm = get_time('%Y-%m-%d')
    return f'files/{tm}/{random_str()}.{frmt}'


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def get_created_at(self):
        return self.created_at.strftime('%Y-%m-%d %H:%M:%S')

    def get_created_at_timepast(self):
        return get_timesince_persian(self.created_at)


class File(models.Model):
    file = models.FileField(upload_to=upload_file_src, max_length=400, null=True)

    class Meta:
        ordering = '-id',
        abstract = True

    def __str__(self):
        return f'#{self.id} File'


# ---

class Department(BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Project(BaseModel):
    name = models.CharField(max_length=100)
    task_master = models.CharField(max_length=100)
    time_start = models.DateTimeField()
    time_end = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Task(BaseModel):
    # STATUS_OPTIONS = (
    #     ('finished', 'انجام شد'),
    #     ('follow-up', 'پیگیری'),
    #     ('allocation', 'تخصیص'),
    # )
    STATE_OPTIONS = (
        ('finished', 'انجام شد'),
        ('progress', 'در حال انجام'),
        ('queue', 'در صف'),
        ('hold', 'نگه داشته شده'),
        ('need-to-check', 'نیاز به بررسی'),
    )
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    description_allocate = models.TextField(null=True, blank=True)
    # status = models.CharField(max_length=20, choices=STATUS_OPTIONS,default='allocation')
    state = models.CharField(max_length=20, choices=STATE_OPTIONS, default='queue')
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    allocator_user = models.ForeignKey('account.User', on_delete=models.CASCADE)
    allocator_department = models.ForeignKey('Department', on_delete=models.CASCADE)
    work_hour = models.IntegerField()
    time_start = models.DateTimeField()
    time_end = models.DateTimeField()
    priority = models.IntegerField(default=1)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class TaskStatus(BaseModel, File):
    STATUS_OPTIONS = (
        ('accepted', 'تایید شد'),
        ('rejected', 'رد شد'),
    )
    status = models.CharField(max_length=20, choices=STATUS_OPTIONS)
    description = models.TextField()

    def __str__(self):
        return self.status


class Inquiry(BaseModel):
    inquiry_user = models.ForeignKey('account.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.title


class InquiryStatus(BaseModel, File):
    STATUS_OPTIONS = (
        ('accepted', 'تایید شد'),
        ('rejected', 'رد شد'),
    )
    status = models.CharField(max_length=20, choices=STATUS_OPTIONS)
    inquiry = models.ForeignKey('Inquiry', on_delete=models.CASCADE)
    description = models.TextField()

    def __str__(self):
        return self.status


