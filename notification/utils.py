from .models import NotificationDepartment


def create_notification(title: str, from_department: object, to_departments: list, projects: list,
                        **kwargs):
    kwargs.setdefault('projects_type', 'selected')
    n = NotificationDepartment.objects.create(
        title=title,
        from_department=from_department,
        **kwargs
    )
    n.projects.set(projects)
    n.to_departments.set(to_departments)
    n.to_departments.set(to_departments)
    return True
