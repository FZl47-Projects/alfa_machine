# Generated by Django 4.1 on 2023-08-17 14:58

import core.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('public', '0010_project_is_paid'),
    ]

    operations = [
        migrations.CreateModel(
            name='NotificationDepartment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('file', models.FileField(blank=True, max_length=400, null=True, upload_to=core.models.upload_file_src)),
                ('title', models.CharField(max_length=150)),
                ('description', models.TextField(blank=True, null=True)),
                ('priority', models.IntegerField(default=1)),
                ('from_department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_dp_notification', to='public.department')),
                ('to_department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_dp_notification', to='public.department')),
            ],
            options={
                'ordering': ('-id',),
            },
        ),
    ]
