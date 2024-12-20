# Generated by Django 4.2 on 2024-05-15 14:50

from django.db import migrations, models
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0004_remove_task_file_projectfile_task'),
    ]

    operations = [
        # migrations.AddField(
        #     model_name='projectfile',
        #     name='to_departments',
        #     field=models.ManyToManyField(related_name='departments_access', to='public.department'),
        # ),
        migrations.AlterField(
            model_name='inquiry',
            name='time_deadline_response',
            field=django_jalali.db.models.jDateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='inquiry',
            name='time_receive',
            field=django_jalali.db.models.jDateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='inquiry',
            name='time_submit',
            field=django_jalali.db.models.jDateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='mass_delivery_date',
            field=django_jalali.db.models.jDateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='sample_delivery_date',
            field=django_jalali.db.models.jDateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='time_end',
            field=django_jalali.db.models.jDateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='time_start',
            field=django_jalali.db.models.jDateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='time_end',
            field=django_jalali.db.models.jDateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='time_start',
            field=django_jalali.db.models.jDateField(blank=True, null=True),
        ),
    ]
