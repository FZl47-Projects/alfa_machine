# Generated by Django 4.2 on 2023-11-14 23:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0028_taskmaster_alter_project_task_master'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='inquiry',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='public.inquiry'),
        ),
    ]
