# Generated by Django 4.1 on 2023-08-21 22:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0014_inquiry_from_department'),
        ('support', '0002_remove_ticketdepartment_to_department_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticketdepartment',
            name='project',
        ),
        migrations.AddField(
            model_name='ticketdepartment',
            name='projects',
            field=models.ManyToManyField(to='public.project'),
        ),
    ]
