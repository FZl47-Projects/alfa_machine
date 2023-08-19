from django.db import models
from core.models import BaseModel, File


class MaterialProject(BaseModel):
    project = models.OneToOneField('public.Project', on_delete=models.CASCADE)
    items = models.ManyToManyField('MaterialItem')
    delivery_status = models.BooleanField(default=False)

    def __str__(self):
        return 'material projeect'


class MaterialQualityProject(BaseModel, File):
    project = models.ForeignKey('public.Project', on_delete=models.CASCADE)
    description = models.TextField()

    def __str__(self):
        return f'#{self.id}'


class MaterialQuality(BaseModel, File):
    items = models.ManyToManyField('MaterialItem')
    description = models.TextField()

    def __str__(self):
        return f'#{self.id}'


class MaterialItem(BaseModel):
    name = models.CharField(max_length=150)
    receiver = models.CharField(max_length=100)
    time_enter = models.DateField()
    time_leave = models.DateField()
    description = models.TextField()
    code = models.CharField(max_length=30)
    size = models.CharField(max_length=30)
    amount = models.BigIntegerField()
    amount_withdrawable = models.BigIntegerField()
    amount_allocated = models.BigIntegerField()
    is_checked = models.BooleanField(default=False)

    class Meta:
        ordering = '-id',

    def __str__(self):
        return self.name

    def get_time_enter(self):
        return self.time_enter.strftime('%Y-%m-%d')

    def get_time_leave(self):
        return self.time_leave.strftime('%Y-%m-%d')

    def has_quality_passed(self):
        return True if self.materialquality_set.count() > 0 else False
