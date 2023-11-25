""" Django-q tasks module """

from django.utils import timezone
from notification.models import NotificationDepartment
from departments.financial.models import SuretyBond


# Send reminder notif on time
def send_reminder_notif(from_department, department):
    now = timezone.now().date()
    surety_bonds = SuretyBond.objects.filter(reminder_time__lt=now)

    for surety_bond in surety_bonds:

        NotificationDepartment.objects.create(
            from_department=from_department,
            title='یادآوری حسن انجام کار',
            description=f'تاریخ حسن انجام کار برای {surety_bond.project.name} فرارسیده است. ',
            department=department,
            projects=[],
        )
