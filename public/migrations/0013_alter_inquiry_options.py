# Generated by Django 4.1 on 2023-08-19 15:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0012_remove_inquiry_inquiry_user_inquiry_time_submited_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='inquiry',
            options={'ordering': ('-id',)},
        ),
    ]
