# Generated by Django 4.2 on 2023-11-14 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0026_alter_inquiry_state'),
        ('support', '0008_alter_report_code_alter_report_projects'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticketdepartment',
            name='projects',
            field=models.ManyToManyField(blank=True, to='public.project'),
        ),
    ]
