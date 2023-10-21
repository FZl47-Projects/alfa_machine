# Generated by Django 4.1 on 2023-10-22 01:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0016_alter_project_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='status',
            field=models.CharField(choices=[('paused', 'متوقف شده'), ('under_construction', 'در حال ساخت')], default='under_construction', max_length=20),
        ),
    ]
