# Generated by Django 4.2 on 2023-11-15 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0030_alter_project_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='time_end',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='time_start',
            field=models.DateField(null=True),
        ),
    ]
