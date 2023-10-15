from django.db import models
from core.models import BaseModel, File


class TicketDepartment(BaseModel, File):
    description = models.TextField()
    from_department = models.ForeignKey('public.Department', on_delete=models.CASCADE, related_name='from_dp')
    departments = models.ManyToManyField('public.Department')
    projects = models.ManyToManyField('public.Project')
    is_open = models.BooleanField(default=True)
    is_all_departments = models.BooleanField(default=True)
    is_all_projects = models.BooleanField(default=True)

    class Meta:
        ordering = '-id',

    def __str__(self):
        return self.description[:20]

    def get_projects_name(self):
        p = self.projects.values_list('name', flat=True)
        return p


class Report(BaseModel, File):
    description = models.TextField()
    from_department = models.ForeignKey('public.Department', on_delete=models.CASCADE, related_name='report_from_dp')
    departments = models.ManyToManyField('public.Department')
    projects = models.ManyToManyField('public.Project')
    is_all_departments = models.BooleanField(default=True)
    is_all_projects = models.BooleanField(default=True)

    class Meta:
        ordering = '-id',

    def __str__(self):
        return self.description[:20]

    def get_projects_name(self):
        p = self.projects.values_list('name', flat=True)
        return p
