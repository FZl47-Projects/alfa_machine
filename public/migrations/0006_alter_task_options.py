# Generated by Django 4.1 on 2023-08-16 20:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0005_taskstatus_task'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='task',
            options={'ordering': ('-id',)},
        ),
    ]
