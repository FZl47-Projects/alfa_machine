from django.contrib import admin
from . import models

admin.site.register(models.NotificationDepartment)
admin.site.register(models.NotificationDepartmentSeen)

