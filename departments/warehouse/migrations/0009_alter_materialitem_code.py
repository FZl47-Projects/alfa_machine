# Generated by Django 4.1 on 2023-08-17 23:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0008_remove_materialquality_material_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='materialitem',
            name='code',
            field=models.CharField(max_length=30),
        ),
    ]
