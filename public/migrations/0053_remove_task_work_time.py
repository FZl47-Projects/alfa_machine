# Generated by Django 4.2 on 2024-01-24 03:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0052_alter_taskstatus_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='work_time',
        ),
    ]