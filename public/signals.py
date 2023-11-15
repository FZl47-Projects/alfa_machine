from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Task


@receiver(pre_save, sender=Task)
def update_state_time(sender, instance, *args, **kwargs):
    if instance.pk:
        original_instance = sender.objects.get(pk=instance.pk)

        if original_instance.state != instance.state:
            instance.state_modify_time = timezone.now()
