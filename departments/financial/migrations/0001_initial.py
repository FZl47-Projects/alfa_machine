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
            name='SuretyBond',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('file', models.FileField(blank=True, max_length=400, null=True, upload_to=core.models.upload_file_src)),
                ('number_id', models.CharField(blank=True, max_length=40, null=True)),
                ('status', models.CharField(choices=[('free', 'ازاد'), ('restricted', 'قفل')], max_length=12)),
                ('description', models.TextField(blank=True, null=True)),
                ('project', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='public.project')),
            ],
            options={
                'ordering': ('-id',),
            },
            bases=(core.mixins.RemoveOldFileMixin, models.Model),
        ),
        migrations.CreateModel(
            name='ReminderProject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('time', models.DateField()),
                ('description', models.TextField(blank=True, null=True)),
                ('project', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='public.project')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('file', models.FileField(blank=True, max_length=400, null=True, upload_to=core.models.upload_file_src)),
                ('tracking_code', models.CharField(max_length=100)),
                ('type_payment', models.CharField(choices=[('prepayment', 'پیش پرداخت'), ('payment', 'پرداخت')], max_length=20)),
                ('type_status_payment', models.CharField(choices=[('deposit', 'واریزی'), ('payment', 'پرداختی')], max_length=20)),
                ('price', models.BigIntegerField()),
                ('submited_at', models.DateField()),
                ('description', models.TextField(blank=True, null=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='public.project')),
            ],
            options={
                'ordering': ('-id',),
            },
            bases=(core.mixins.RemoveOldFileMixin, models.Model),
        ),
    ]
