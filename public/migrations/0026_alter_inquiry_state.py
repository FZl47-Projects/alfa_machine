# Generated by Django 4.2 on 2023-11-13 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0025_alter_project_number_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inquiry',
            name='state',
            field=models.CharField(choices=[('canceled', 'انصراف'), ('waiting_for_price', 'در انتظار قیمت'), ('price_recorded', 'قیمت ارسال شده')], max_length=20),
        ),
    ]
