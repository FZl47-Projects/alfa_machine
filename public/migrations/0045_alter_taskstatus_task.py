# Generated by Django 4.2 on 2024-01-17 20:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0044_remove_task_state_remove_task_state_modify_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskstatus',
            name='task',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='public.task'),
        ),
    ]
