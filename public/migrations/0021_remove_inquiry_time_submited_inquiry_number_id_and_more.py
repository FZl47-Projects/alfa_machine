# Generated by Django 4.1 on 2023-10-23 01:31

import core.models
import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0020_alter_task_time_end_alter_task_time_start'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inquiry',
            name='time_submited',
        ),
        migrations.AddField(
            model_name='inquiry',
            name='number_id',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='inquiry',
            name='sender',
            field=models.CharField(default='-', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='inquiry',
            name='state',
            field=models.CharField(choices=[('canceled', 'انصارف'), ('waiting_for_price', 'در انتظار قیمت'), ('price_recorded', 'قیمت ارسال شده')], default='price_recorded', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='inquiry',
            name='time_deadline_response',
            field=models.DateField(default=datetime.datetime(2023, 10, 23, 1, 31, 36, 658499)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='inquiry',
            name='time_receive',
            field=models.DateField(default=datetime.datetime(2023, 10, 23, 1, 31, 42, 522773)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='inquiry',
            name='time_submit',
            field=models.DateField(default=datetime.datetime(2023, 10, 23, 1, 31, 47, 91999)),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='inquiry',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.CreateModel(
            name='InquiryFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('file', models.FileField(blank=True, max_length=400, null=True, upload_to=core.models.upload_file_src)),
                ('description', models.TextField(null=True)),
                ('departments', models.ManyToManyField(to='public.department')),
                ('inquiry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='public.inquiry')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
