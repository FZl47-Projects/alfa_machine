# Generated by Django 4.1 on 2023-10-25 03:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0023_inquiryfile_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='inquiry',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='public.inquiry'),
        ),
    ]