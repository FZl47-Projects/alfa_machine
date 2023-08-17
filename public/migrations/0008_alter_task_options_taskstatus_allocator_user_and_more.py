# Generated by Django 4.1 on 2023-08-16 23:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('public', '0007_alter_inquirystatus_inquiry'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='task',
            options={'ordering': ('priority', '-id')},
        ),
        migrations.AddField(
            model_name='taskstatus',
            name='allocator_user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='taskstatus',
            name='task',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='status', to='public.task'),
        ),
    ]
