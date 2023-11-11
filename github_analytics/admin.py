from django.contrib import admin
from .models import UserProfile, Repository, CommitData, PullRequestData, IssueData, ContributorData

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Repository)
admin.site.register(CommitData)
admin.site.register(PullRequestData)
admin.site.register(IssueData)
admin.site.register(ContributorData)