# Generated by Django 4.2 on 2024-01-22 02:39

from django.db import migrations, models
import django.db.models.deletion
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0045_alter_taskstatus_task'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskstatus',
            name='department',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='public.department'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='project',
            name='time_start',
            field=django_jalali.db.models.jDateField(blank=True, null=True),
        ),
    ]