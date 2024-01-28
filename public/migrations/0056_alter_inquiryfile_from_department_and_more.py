# Generated by Django 4.2 on 2024-01-27 22:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0055_file_remove_inquiryfile_file_inquiryfile_files'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inquiryfile',
            name='from_department',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='inquiry_file_from_dep', to='public.department'),
        ),
        migrations.AlterField(
            model_name='inquiryfile',
            name='to_departments',
            field=models.ManyToManyField(related_name='inquiry_file_to_dep', to='public.department'),
        ),
    ]
