# Generated by Django 4.2 on 2024-01-30 02:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0013_notificationdepartment_attached_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notificationdepartment',
            name='attached_link',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
