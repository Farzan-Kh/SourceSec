# Generated by Django 4.2 on 2025-01-28 11:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('staticAnalysis', '0004_delete_snippetsnapshot'),
    ]

    operations = [
        migrations.CreateModel(
            name='RepoProject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CodeProject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='projectsnapshot',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='staticAnalysis.codeproject'),
        ),
        migrations.AlterField(
            model_name='reposnapshot',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='staticAnalysis.repoproject'),
        ),
        migrations.DeleteModel(
            name='Project',
        ),
    ]
