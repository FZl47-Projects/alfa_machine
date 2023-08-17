from django.db import models
from core.models import BaseModel, File


class Material(BaseModel):
    project = models.ForeignKey('public.Project', on_delete=models.CASCADE)
    items = models.ManyToManyField('MaterialItem')
    time_end = models.DateTimeField()
    delivery_status = models.BooleanField()

    def __str__(self):
        return self.project


class MaterialQuality(BaseModel, File):
    material = models.ForeignKey('Material', on_delete=models.CASCADE)
    description = models.TextField()

    def __str__(self):
        return self.material


class MaterialItem(BaseModel):
    name = models.CharField(max_length=150)
    amount = models.BigIntegerField()

    def __str__(self):
        return self.name
