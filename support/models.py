from django.db import models
from core.models import BaseModel, FileAbstract
from core.utils import get_random_code
from public.models import Project, Department


class TicketDepartment(BaseModel, FileAbstract):
    description = models.TextField()
    from_department = models.ForeignKey('public.Department', on_delete=models.CASCADE, related_name='from_dp')
    department = models.ForeignKey('public.Department', on_delete=models.CASCADE, related_name='ticket_departments')
    projects = models.ManyToManyField('public.Project', blank=True)
    is_open = models.BooleanField(default=True)
    # is_all_departments = models.BooleanField(default=True)
    is_all_projects = models.BooleanField(default=True)
    seen = models.BooleanField(default=False)

    class Meta:
        ordering = '-id',

    def __str__(self):
        return self.description[:20]

    def get_projects_name(self):
        p = self.projects.values_list('name', flat=True)
        if p:
            return p
        return None

    def get_departments_list(self):
        departments = Department.objects.filter(ticket_departments__description=self.description)
        return departments.values_list('name', flat=True)


class Report(BaseModel, FileAbstract):
    code = models.CharField('Report Code', default='', max_length=12, unique=True, blank=True)
    description = models.TextField()
    from_department = models.ForeignKey('public.Department', on_delete=models.CASCADE, related_name='report_from_dp')
    departments = models.ManyToManyField('public.Department')
    projects = models.ManyToManyField('public.Project', blank=True)
    is_all_departments = models.BooleanField(default=True)
    is_all_projects = models.BooleanField(default=True)

    class Meta:
        ordering = '-id',

    def __str__(self):
        return self.description[:20]

    def save(self, *args, **kwargs):
        # Ensure the report_code is generated even if not provided
        if not self.code:
            self.code = self.create_unique_code()

        super().save(*args, **kwargs)

    def create_unique_code(self):
        # Generate a random 12-digit code
        new_code = get_random_code(12)

        while Report.objects.filter(code=new_code).exists():
            # Check if the generated code is unique
            new_code = get_random_code(12)

        return new_code

    def get_projects_name(self):
        p = self.projects.values_list('name', flat=True)
        if not p:
            return None
        return p
