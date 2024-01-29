from django.db import models
from core.models import BaseModel, FileAbstract
from public.models import Project, Department
from core.utils import random_int


class TicketDepartment(BaseModel, FileAbstract):
    PROJECTS_TYPE_OPTIONS = (
        ('selected', 'انتخاب شده'),
        ('other', 'متفرقه'),
    )

    number_id = models.CharField(max_length=10, default=random_int)
    title = models.CharField(max_length=150)
    description = models.TextField(null=True)
    from_department = models.ForeignKey('public.Department', on_delete=models.CASCADE, related_name='from_dep_ticket')
    to_departments = models.ManyToManyField('public.Department', related_name='to_deps_ticket')
    projects_type = models.CharField(max_length=10, choices=PROJECTS_TYPE_OPTIONS)
    projects = models.ManyToManyField('public.Project')
    is_open = models.BooleanField(default=True)

    class Meta:
        ordering = '-id',

    def __str__(self):
        return self.title

    def get_projects(self):
        return self.projects.all()

    def get_to_departments(self):
        return self.to_departments.all()
