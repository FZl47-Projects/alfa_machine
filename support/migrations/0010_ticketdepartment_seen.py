# Generated by Django 4.2 on 2023-11-21 00:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0009_alter_ticketdepartment_projects'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticketdepartment',
            name='seen',
            field=models.BooleanField(default=False),
        ),
    ]
