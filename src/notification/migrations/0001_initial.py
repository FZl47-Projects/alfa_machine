# Generated by Django 4.2 on 2024-02-07 02:50

import core.mixins
import core.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('public', '0001_initial'),
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
                ('projects_type', models.CharField(choices=[('selected', 'انتخاب شده'), ('other', 'متفرقه')], max_length=10)),
                ('priority', models.IntegerField(default=1)),
                ('attached_link', models.CharField(blank=True, max_length=200, null=True)),
                ('from_department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_dp_notification', to='public.department')),
                ('projects', models.ManyToManyField(blank=True, to='public.project')),
                ('to_departments', models.ManyToManyField(related_name='to_dp_notification', to='public.department')),
            ],
            options={
                'ordering': ('priority', '-id'),
            },
            bases=(core.mixins.RemoveOldFileMixin, models.Model),
        ),
        migrations.CreateModel(
            name='NotificationDepartmentSeen',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='public.department')),
                ('notification', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seen_status', to='notification.notificationdepartment')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
