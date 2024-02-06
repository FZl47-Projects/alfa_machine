# Generated by Django 4.2 on 2024-02-07 02:50

import core.mixins
import core.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, max_length=400, null=True, upload_to=core.models.upload_file_src)),
            ],
            options={
                'ordering': ('-id',),
            },
            bases=(core.mixins.RemoveOldFileMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Inquiry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('number_id', models.CharField(blank=True, max_length=32, null=True)),
                ('state', models.CharField(blank=True, choices=[('canceled', 'انصراف'), ('waiting_for_price', 'در انتظار قیمت'), ('price_recorded', 'قیمت ارسال شده')], default='waiting_for_price', max_length=32)),
                ('description', models.TextField(blank=True, null=True)),
                ('time_receive', models.DateField(blank=True, null=True)),
                ('time_deadline_response', models.DateField(blank=True, null=True)),
                ('time_submit', models.DateField(blank=True, null=True)),
                ('from_department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='public.department')),
            ],
            options={
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('number_id', models.CharField(blank=True, max_length=150, null=True)),
                ('prepayment_datetime', models.DateField(blank=True, null=True)),
                ('item', models.TextField(blank=True, null=True)),
                ('count_remaining', models.BigIntegerField()),
                ('count_total', models.BigIntegerField()),
                ('has_sample', models.BooleanField(default=False)),
                ('sample_delivery_date', models.DateField(blank=True, null=True)),
                ('mass_delivery_date', models.DateField(blank=True, null=True)),
                ('name', models.CharField(max_length=100)),
                ('time_start', models.DateField(blank=True, null=True)),
                ('time_end', models.DateField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('price', models.BigIntegerField(blank=True, null=True)),
                ('is_paid', models.BooleanField(default=False)),
                ('description', models.TextField(blank=True, null=True)),
                ('status', models.CharField(choices=[('checking', 'در حال بررسی قبل ساخت'), ('under_construction', 'در حال ساخت'), ('posted', 'ارسال شده'), ('completed', 'تایید و اتمام'), ('paused', 'متوقف شده')], default='under_construction', max_length=20)),
                ('progress_percentage', models.PositiveSmallIntegerField(default=0)),
                ('inquiry', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='public.inquiry')),
            ],
            options={
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('file', models.FileField(blank=True, max_length=400, null=True, upload_to=core.models.upload_file_src)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('time_start', models.DateField(null=True)),
                ('time_end', models.DateField(null=True)),
                ('priority', models.IntegerField(default=1)),
                ('is_active', models.BooleanField(default=True)),
                ('allocator_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('from_department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_department', to='public.department')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='public.project')),
                ('to_department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='public.department')),
            ],
            options={
                'ordering': ('priority', '-id'),
            },
            bases=(core.mixins.RemoveOldFileMixin, models.Model),
        ),
        migrations.CreateModel(
            name='TaskMaster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=128, verbose_name='Task Master name')),
                ('description', models.TextField(null=True)),
            ],
            options={
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='TaskStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('file', models.FileField(blank=True, max_length=400, null=True, upload_to=core.models.upload_file_src)),
                ('status', models.CharField(choices=[('finished', 'انجام شد'), ('progress', 'در حال انجام'), ('queue', 'در صف'), ('hold', 'نگه داشته شده'), ('need-to-check', 'نیاز به بررسی'), ('need-to-replan', 'نیاز به برنامه ریزی مجدد')], max_length=20)),
                ('description', models.TextField(null=True)),
                ('allocator_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='public.department')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='public.task')),
            ],
            options={
                'ordering': ('-id',),
            },
            bases=(core.mixins.RemoveOldFileMixin, models.Model),
        ),
        migrations.CreateModel(
            name='ProjectStep',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('person_traffic', models.CharField(choices=[('person/day', 'نفر/روز'), ('person/hour', 'نفر/ساعت')], max_length=15)),
                ('plan', models.IntegerField()),
                ('actual', models.IntegerField(null=True)),
                ('description', models.TextField(null=True)),
                ('from_department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='public.department')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='public.project')),
            ],
            options={
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='ProjectNote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('text', models.TextField()),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='public.project')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='ProjectFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('file', models.FileField(blank=True, max_length=400, null=True, upload_to=core.models.upload_file_src)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(null=True)),
                ('allocator_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('from_department', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='public.department')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='public.project')),
            ],
            options={
                'ordering': ('-id',),
            },
            bases=(core.mixins.RemoveOldFileMixin, models.Model),
        ),
        migrations.AddField(
            model_name='project',
            name='task_master',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='projects', to='public.taskmaster'),
        ),
        migrations.CreateModel(
            name='InquiryStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('file', models.FileField(blank=True, max_length=400, null=True, upload_to=core.models.upload_file_src)),
                ('status', models.CharField(choices=[('accepted', 'تایید شده'), ('rejected', 'رد شده')], max_length=20)),
                ('description', models.TextField()),
                ('inquiry', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='status', to='public.inquiry')),
            ],
            options={
                'abstract': False,
            },
            bases=(core.mixins.RemoveOldFileMixin, models.Model),
        ),
        migrations.CreateModel(
            name='InquiryFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(null=True)),
                ('allocator_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('files', models.ManyToManyField(to='public.file')),
                ('from_department', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='inquiry_file_from_dep', to='public.department')),
                ('inquiry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='public.inquiry')),
                ('to_departments', models.ManyToManyField(related_name='inquiry_file_to_dep', to='public.department')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='inquiry',
            name='task_master',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='public.taskmaster'),
        ),
    ]
