from django.db import models
from django.urls import reverse
from core.models import BaseModel, FileAbstract


class ItemWarehouse(BaseModel):
    name = models.CharField(max_length=100)
    project = models.ForeignKey('public.Project', on_delete=models.CASCADE)
    price = models.BigIntegerField(default=0)
    register_time = models.DateField()
    description = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return f'register item | {self.name}'

    @classmethod
    def has_perm_to_modify(cls, user):
        if user.is_anonymous:
            return False
        if user.role in ('warehouse_user', 'super_user'):
            return True
        return False

    def get_absolute_url(self):
        return reverse('dp_warehouse:item__detail', args=(self.id,))

    def get_files(self):
        return self.itemfile_set.all()


class ItemFile(BaseModel, FileAbstract):
    from_department = models.ForeignKey('public.Department', on_delete=models.CASCADE)
    register_warehouse = models.ForeignKey(ItemWarehouse, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return f'register item file | {self.register_warehouse.name}'
