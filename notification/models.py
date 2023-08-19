from django.db import models
from core.models import BaseModel, File


class NotificationDepartment(BaseModel, File):
    from_department = models.ForeignKey('public.Department', on_delete=models.CASCADE,
                                        related_name='from_dp_notification')
    to_department = models.ForeignKey('public.Department', on_delete=models.CASCADE, related_name='to_dp_notification')
    project = models.ForeignKey('public.Project', on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    description = models.TextField(null=True, blank=True)
    priority = models.IntegerField(default=1)

    class Meta:
        ordering = '-id',

    def __str__(self):
        return self.title or 'notification'

    def get_title(self):
        return self.title or 'notification'
