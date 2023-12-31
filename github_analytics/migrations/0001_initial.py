# Generated by Django 4.2.6 on 2023-10-27 05:05

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
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('github_username', models.CharField(max_length=255, unique=True)),
                ('avatar_url', models.URLField(blank=True, max_length=500)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Repository',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('github_repo_id', models.PositiveIntegerField(unique=True)),
                ('name', models.CharField(max_length=255)),
                ('repository_url', models.URLField(max_length=500)),
                ('description', models.TextField(blank=True)),
                ('user_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='github_analytics.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='PullRequestData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateField()),
                ('date_merged', models.DateField(blank=True, null=True)),
                ('title', models.CharField(max_length=500)),
                ('status', models.CharField(max_length=100)),
                ('repository', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='github_analytics.repository')),
            ],
        ),
        migrations.CreateModel(
            name='IssueData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateField()),
                ('date_closed', models.DateField(blank=True, null=True)),
                ('title', models.CharField(max_length=500)),
                ('status', models.CharField(max_length=100)),
                ('repository', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='github_analytics.repository')),
            ],
        ),
        migrations.CreateModel(
            name='ContributorData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contributions_count', models.PositiveIntegerField()),
                ('contributor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='github_analytics.userprofile')),
                ('repository', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='github_analytics.repository')),
            ],
        ),
        migrations.CreateModel(
            name='CommitData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('commit_count', models.PositiveIntegerField()),
                ('repository', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='github_analytics.repository')),
            ],
        ),
    ]
