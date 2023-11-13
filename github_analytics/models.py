from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Repository(models.Model):
    github_repo_id = models.PositiveIntegerField(unique=True)
    name = models.CharField(max_length=255)
    repository_url = models.URLField(max_length=500)
    description = models.TextField(blank=True,null=True)

class CommitData(models.Model):
    repository = models.ForeignKey(Repository, to_field='github_repo_id', on_delete=models.CASCADE)
    date = models.DateTimeField()

class PullRequestData(models.Model):
    repository = models.ForeignKey(Repository, to_field='github_repo_id', on_delete=models.CASCADE)
    date_created = models.DateTimeField()
    date_merged = models.DateTimeField(blank=True, null=True)
    title = models.CharField(max_length=500)
    status = models.CharField(max_length=100) # such "open", "closed", "merged"

class IssueData(models.Model):
    repository = models.ForeignKey(Repository, to_field='github_repo_id', on_delete=models.CASCADE)
    date_created = models.DateTimeField()
    date_closed = models.DateTimeField(blank=True, null=True) 
    title = models.CharField(max_length=500)
    status = models.CharField(max_length=100) # such "open", "closed"

class UserProfile(models.Model):
    github_username = models.CharField(max_length=255, unique=True)
    avatar_url = models.URLField(max_length=500, blank=True)

class ContributorData(models.Model):
    repository = models.ForeignKey(Repository, to_field='github_repo_id', on_delete=models.CASCADE)
    contributor = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True) 
    contributions_count = models.PositiveIntegerField()

