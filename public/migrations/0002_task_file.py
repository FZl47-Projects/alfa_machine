# Generated by Django 4.1 on 2023-08-16 16:25

import core.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='file',
            field=models.FileField(max_length=400, null=True, upload_to=core.models.upload_file_src),
        ),
    ]
