# Generated by Django 4.1 on 2023-10-30 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0024_project_inquiry'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='number_id',
            field=models.CharField(max_length=150),
        ),
    ]
