# Generated by Django 4.2 on 2024-01-22 02:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0047_auto_20240122_0240'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='time_start',
            field=models.DateField(blank=True, null=True),
        ),
    ]
