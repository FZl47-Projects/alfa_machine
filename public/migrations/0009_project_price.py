# Generated by Django 4.1 on 2023-08-16 23:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0008_alter_task_options_taskstatus_allocator_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='price',
            field=models.BigIntegerField(default=1),
            preserve_default=False,
        ),
    ]
