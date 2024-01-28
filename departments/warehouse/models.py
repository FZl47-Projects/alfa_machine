from django.db import models
from core.models import BaseModel, FileAbstract


# WarehouseRegistrations model
class WarehouseRegistration(BaseModel, FileAbstract):
    project = models.ForeignKey('public.Project', on_delete=models.CASCADE, related_name='warehouse_registrations')
    price = models.BigIntegerField(default=0)
    register_time = models.DateTimeField()
    description = models.TextField(null=True, blank=True)

    class Meta:
        ordering = '-id',

    def __str__(self):
        return self.project.name

    def get_register_time(self):
        if self.register_time:
            return self.register_time.strftime('%Y-%m-%d %H:%M')


# RegistrationFiles model
class RegistrationFile(BaseModel, FileAbstract):
    warehouse_register = models.OneToOneField(WarehouseRegistration, on_delete=models.CASCADE, related_name='registration_file')

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return f'{self.warehouse_register.project.name} - {self.warehouse_register.register_time}'
