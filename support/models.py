from django.db import models
from django.urls import reverse
from core.models import BaseModel, FileAbstract
from core.utils import random_int
from public.models import Project, Department


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

    def has_perm_to_modify(self, user):
        if user.is_anonymous:
            return False
        if user.department == self.from_department or user.role in ('super_user',):
            return True
        return False

    def get_projects(self):
        return self.projects.all()

    def get_to_departments(self):
        return self.to_departments.all()

    def get_absolute_url(self):
        return reverse('support:ticket__detail', args=(self.id,))
