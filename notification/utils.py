from public.models import Department, Project
from .models import NotificationDepartment


# Create notif for departments
def create_notification(from_department=None, title=None, description=None, projects=None, departments: list = None,
                        all_departments: bool = False, all_projects: bool = False, **kwargs):
    """ Create notification for each department. return True if everything goes well. """

    if all_departments:
        departments = Department.objects.all()
    if all_projects:
        projects = Project.objects.filter(is_active=True)

    for department in departments:
        notif = NotificationDepartment.objects.create(
            from_department=from_department,
            department=department,
            title=title,
            description=description
        )
        notif.projects.set([projects])

    return True
