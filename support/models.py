from django.db import models
from core.models import BaseModel, File


class TicketDepartment(BaseModel, File):
    description = models.TextField()
    department = models.ForeignKey('core.Department', on_delete=models.CASCADE)
    project = models.ForeignKey('core.Project', on_delete=models.CASCADE)
    is_open = models.BooleanField(default=True)

    def __str__(self):
        return self.description[:20]
