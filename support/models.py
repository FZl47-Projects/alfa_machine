from django.db import models
from core.models import BaseModel, File


class TicketDepartment(BaseModel, File):
    description = models.TextField()
    from_department = models.ForeignKey('public.Department', on_delete=models.CASCADE,related_name='from_dp')
    to_department = models.ForeignKey('public.Department', on_delete=models.CASCADE,related_name='to_dp')
    project = models.ForeignKey('public.Project', on_delete=models.CASCADE)
    is_open = models.BooleanField(default=True)

    def __str__(self):
        return self.description[:20]
