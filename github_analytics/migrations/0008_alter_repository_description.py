# Generated by Django 4.2.6 on 2023-11-11 03:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('github_analytics', '0007_remove_commitdata_commit_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='repository',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
