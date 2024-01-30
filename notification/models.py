from django.db import models
from django.urls import reverse
from core.models import BaseModel, FileAbstract


class NotificationDepartment(BaseModel, FileAbstract):
    PROJECTS_TYPE_OPTIONS = (
        ('selected', 'انتخاب شده'),
        ('other', 'متفرقه'),
    )
    title = models.CharField(max_length=150)
    description = models.TextField(null=True, blank=True)
    from_department = models.ForeignKey('public.Department', on_delete=models.CASCADE,
                                        related_name='from_dp_notification')
    to_departments = models.ManyToManyField('public.Department', related_name='to_dp_notification')
    projects = models.ManyToManyField('public.Project', blank=True)
    projects_type = models.CharField(max_length=10, choices=PROJECTS_TYPE_OPTIONS)
    priority = models.IntegerField(default=1)
    attached_link = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        ordering = 'priority', '-id'

    def __str__(self):
        return self.title

    def has_perm_to_modify(self, user):
        if user.is_anonymous:
            return False
        if user.department == self.from_department or user.role in ('super_user',):
            return True
        return False

    def get_title(self):
        return self.title

    def get_projects(self):
        return self.projects.all()

    def get_to_departments(self):
        return self.to_departments.all()

    def get_departments_seen_status(self):
        return self.seen_status.all().distinct()

    def get_departments_seen_status_dep_ids(self):
        return list(self.get_departments_seen_status().values_list('department_id', flat=True))

    def get_absolute_url(self):
        return reverse('notification:notification__detail', args=(self.id,))


class NotificationDepartmentSeen(BaseModel):
    department = models.ForeignKey('public.Department', on_delete=models.CASCADE)
    notification = models.ForeignKey(NotificationDepartment, on_delete=models.CASCADE, related_name='seen_status')

    def __str__(self): return self.notification.title
