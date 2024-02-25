from notification.utils import create_notification_by_role
from departments.financial.models import ReminderProject
from public.models import Department


def send_reminder_notify_financial_project(reminder_id, from_department_id):
    try:
        reminder = ReminderProject.objects.get(id=reminder_id)
        from_department = Department.objects.get(id=from_department_id)
    except (ReminderProject.DoesNotExist, Department.DoesNotExist):
        return

    create_notification_by_role(
        title='یادآور پروژه',
        from_department=from_department,
        to_users=['financial_user', 'super_user', 'control_project_user'],
        projects=[reminder.project],
        description=reminder.description
    )

    reminder.delete()
