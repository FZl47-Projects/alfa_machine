from django.contrib import admin
from . import models


# Register your models here.
admin.site.register(models.Payment)
admin.site.register(models.PrePayment)
admin.site.register(models.SuretyBond)
