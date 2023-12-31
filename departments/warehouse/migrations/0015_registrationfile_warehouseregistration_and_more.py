# Generated by Django 4.2 on 2023-11-25 02:33

import core.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0039_alter_inquiry_state'),
        ('warehouse', '0014_alter_materialproject_delivery_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegistrationFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('file', models.FileField(blank=True, max_length=400, null=True, upload_to=core.models.upload_file_src)),
            ],
            options={
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='WarehouseRegistration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('file', models.FileField(blank=True, max_length=400, null=True, upload_to=core.models.upload_file_src)),
                ('price', models.BigIntegerField(default=0)),
                ('register_time', models.DateTimeField()),
                ('description', models.TextField(blank=True, null=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='warehouse_registrations', to='public.project')),
            ],
            options={
                'ordering': ('-id',),
            },
        ),
        migrations.RemoveField(
            model_name='materialproject',
            name='items',
        ),
        migrations.RemoveField(
            model_name='materialproject',
            name='project',
        ),
        migrations.RemoveField(
            model_name='materialquality',
            name='items',
        ),
        migrations.RemoveField(
            model_name='materialqualityproject',
            name='project',
        ),
        migrations.DeleteModel(
            name='MaterialItem',
        ),
        migrations.DeleteModel(
            name='MaterialProject',
        ),
        migrations.DeleteModel(
            name='MaterialQuality',
        ),
        migrations.DeleteModel(
            name='MaterialQualityProject',
        ),
        migrations.AddField(
            model_name='registrationfile',
            name='warehouse_register',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='registration_file', to='warehouse.warehouseregistration'),
        ),
    ]
