# Generated by Django 4.2 on 2023-11-25 21:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0039_alter_inquiry_state'),
        ('support', '0010_ticketdepartment_seen'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticketdepartment',
            name='departments',
        ),
        migrations.RemoveField(
            model_name='ticketdepartment',
            name='is_all_departments',
        ),
        migrations.AddField(
            model_name='ticketdepartment',
            name='department',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='public.department'),
            preserve_default=False,
        ),
    ]