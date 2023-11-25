""" Django-q tasks module """

from django.utils import timezone
from notification.models import NotificationDepartment


# Send reminder notif on time
def send_reminder_notif(department, obj):
    reminder_time = obj.reminder_time

    if reminder_time <= timezone.now():
        NotificationDepartment.objects.create(
            from_department=department,
            title='یادآوری حسن انجام کار',
            description=f'تاریخ حسن انجام کار برای {obj.project.name} فرارسیده است. '
        )
