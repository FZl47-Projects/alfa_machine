from django.contrib import admin
from . import models

admin.site.register(models.Department)
admin.site.register(models.TaskMaster)
admin.site.register(models.Project)
admin.site.register(models.Task)
admin.site.register(models.ProjectFile)
admin.site.register(models.InquiryFile)
