# Generated by Django 4.2 on 2023-11-14 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0026_alter_inquiry_state'),
        ('notification', '0004_alter_notificationdepartment_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notificationdepartment',
            name='projects',
            field=models.ManyToManyField(blank=True, to='public.project'),
        ),
    ]