from django.db import models
from core.models import BaseModel, File
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string


class Notification(BaseModel, File):
    to_department = models.ForeignKey('core.Department',on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    description = models.TextField(null=True, blank=True)

    class Meta:
        ordering = '-id',

    def __str__(self):
        return self.title or 'notification'

    def get_title(self):
        return self.title or 'notification'




