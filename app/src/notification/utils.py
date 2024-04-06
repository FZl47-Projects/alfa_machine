from django.contrib.auth import get_user_model
from public.models import Department
from .models import NotificationDepartment

User = get_user_model()


def create_notification(title: str, from_department: object, to_departments: list|tuple|None, projects: list|tuple,
                        **kwargs):
    kwargs.setdefault('projects_type', 'selected')
    n = NotificationDepartment.objects.create(
        title=title,
        from_department=from_department,
        **kwargs
    )
    n.projects.set(projects)
    if not to_departments:
        to_departments = Department.objects.all()
    n.to_departments.set(to_departments)
    return True


def create_notification_by_role(title: str, from_department: object, to_users: list|tuple, projects: list|tuple,
                                **kwargs):
    departments = Department.objects.filter(user__role__in=to_users)
    create_notification(title, from_department, departments, projects, **kwargs)
