from django.db import models
from core.models import BaseModel, File


class NotificationDepartment(BaseModel, File):
    from_department = models.ForeignKey('public.Department', on_delete=models.CASCADE,
                                        related_name='from_dp_notification')
    title = models.CharField(max_length=150)
    description = models.TextField(null=True, blank=True)
    projects = models.ManyToManyField('public.Project')
    departments = models.ManyToManyField('public.Department')
    priority = models.IntegerField(default=1)
    is_showing = models.BooleanField(default=True)
    is_all_departments = models.BooleanField(default=True)
    is_all_projects = models.BooleanField(default=True)

    class Meta:
        ordering = 'priority', '-id'

    def __str__(self):
        return self.title or 'notification'

    def get_title(self):
        return self.title or 'notification'

    def get_projects_name(self):
        return self.projects.filter(is_active=True).values_list('name', flat=True)
