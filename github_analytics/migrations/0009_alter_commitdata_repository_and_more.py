# Generated by Django 4.2.6 on 2023-11-11 06:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('github_analytics', '0008_alter_repository_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commitdata',
            name='repository',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='github_analytics.repository', to_field='github_repo_id'),
        ),
        migrations.AlterField(
            model_name='contributordata',
            name='repository',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='github_analytics.repository', to_field='github_repo_id'),
        ),
        migrations.AlterField(
            model_name='issuedata',
            name='date_closed',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='issuedata',
            name='date_created',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='issuedata',
            name='repository',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='github_analytics.repository', to_field='github_repo_id'),
        ),
        migrations.AlterField(
            model_name='pullrequestdata',
            name='repository',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='github_analytics.repository', to_field='github_repo_id'),
        ),
    ]
