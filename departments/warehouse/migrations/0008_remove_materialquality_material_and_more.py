# Generated by Django 4.1 on 2023-08-17 23:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0007_alter_materialitem_size'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='materialquality',
            name='material',
        ),
        migrations.AddField(
            model_name='materialquality',
            name='items',
            field=models.ManyToManyField(to='warehouse.materialitem'),
        ),
    ]
