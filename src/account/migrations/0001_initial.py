# Generated by Django 4.2 on 2024-02-07 02:50

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('first_name', models.CharField(blank=True, default='بدون نام', max_length=150, verbose_name='first name')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, unique=True, verbose_name='email address')),
                ('role', models.CharField(choices=[('super_user', 'کاربر مدیر'), ('control_project_user', 'کاربر کنترل پروژه'), ('control_quality_user', 'کاربر کنترل کیفی'), ('commerce_user', 'کاربر بازرگانی'), ('procurement_commerce_user', 'کاربر بازرگانی-فروش'), ('financial_user', 'کاربر مالی'), ('warehouse_user', 'کاربر انبار'), ('production_user', 'کابر تولید'), ('technical_user', 'کاربر فنی')], max_length=32)),
            ],
            options={
                'ordering': ('-id',),
            },
        ),
    ]
