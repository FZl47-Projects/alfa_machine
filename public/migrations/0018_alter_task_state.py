# Generated by Django 4.1 on 2023-10-22 01:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0017_project_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='state',
            field=models.CharField(choices=[('finished', 'انجام شد'), ('progress', 'در حال انجام'), ('queue', 'در صف'), ('hold', 'نگه داشته شده'), ('need-to-check', 'نیاز به بررسی'), ('need-to-replan', 'نیاز به برنامه ریزی مجدد')], default='queue', max_length=20),
        ),
    ]
