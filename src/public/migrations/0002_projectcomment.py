# Generated by Django 4.2 on 2024-02-22 21:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('text', models.TextField()),
                ('from_department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_comment_from_dp', to='public.department')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='public.project')),
                ('to_departments', models.ManyToManyField(related_name='project_comment_to_dp', to='public.department')),
            ],
            options={
                'ordering': ('-id',),
            },
        ),
    ]