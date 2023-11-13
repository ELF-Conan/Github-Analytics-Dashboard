from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum,Count
from django.db.models.functions import TruncDay, TruncWeek, TruncMonth
from .models import UserProfile, Repository, CommitData, PullRequestData, IssueData, ContributorData
from .github_api import get_user_repos, get_repo_commits, get_repo_pull_requests, get_repo_issues, get_repo_contributors
from django.contrib import messages
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialAccount, SocialToken
import plotly.offline as pyo
import plotly.graph_objs as go
import plotly.express as px
from datetime import datetime,timedelta
from collections import defaultdict,Counter
import matplotlib.pyplot as plt
from django.conf import settings
from django.core.serializers import serialize
import json,os

# Create your views here.
def home(request):
    return render(request, 'github_analytics/home.html')

def test(request):
    return render(request, 'github_analytics/test.html')

@login_required
def fetch_github_data(request):
    user_token = request.user.socialaccount_set.first().socialtoken_set.first().token

    # Fetch and save user repositories
    repos = get_user_repos(user_token)
    for repo in repos:
        repo_obj, created = Repository.objects.get_or_create(
            github_repo_id=repo["id"],
            defaults={
                "name": repo["name"],
                "repository_url": repo["html_url"],
                "description": repo.get("description", "")
            }
        )

        # Fetch and save commit data
        commits = get_repo_commits(user_token, repo["full_name"])
        for commit in commits:
            commit_date = datetime.strptime(commit['commit']['author']['date'], '%Y-%m-%dT%H:%M:%SZ').date()
            CommitData.objects.get_or_create(
                repository=repo_obj,
                date=commit_date,  
            )

        # Fetch and save pull request data
        prs = get_repo_pull_requests(user_token, repo["full_name"])
        for pr in prs:
            PullRequestData.objects.get_or_create(
                repository=repo_obj,
                date_created=pr["created_at"],
                defaults={
                    "date_merged": pr["merged_at"],
                    "title": pr["title"],
                    "status": pr["state"]
                }
            )

        # Fetch and save issue data
        issues = get_repo_issues(user_token, repo["full_name"])
        for issue in issues:
            if "pull_request" not in issue:  # Exclude pull requests
                IssueData.objects.get_or_create(
                    repository=repo_obj,
                    date_created=issue["created_at"],
                    defaults={
                        "date_closed": issue["closed_at"],
                        "title": issue["title"],
                        "status": issue["state"]
                    }
                )

        # Fetch and save contributor data
        contributors = get_repo_contributors(user_token, repo["full_name"])
        for contributor in contributors:
            contributor_profile, created = UserProfile.objects.get_or_create(
                github_username=contributor["login"],
                defaults={"avatar_url": contributor["avatar_url"]}
            )
            ContributorData.objects.get_or_create(
                repository=repo_obj,
                contributor=contributor_profile,
                defaults={"contributions_count": contributor["contributions"]}
            )

####### Create a visual view
def visualize_repositories(request):
    repos = Repository.objects.all()
    return render(request, 'github_analytics/visualize_repositories.html', {'repos': repos})

def commit_frequency(request, repo_id):
    repo = get_object_or_404(Repository, github_repo_id=repo_id)

    # Assume default frequency is daily
    frequency = request.GET.get('frequency', 'Daily')

    # Fetching commit data based on the selected frequency
    if frequency == 'Daily':
        data = CommitData.objects.annotate(commit_count=Count('date'))
    elif frequency == 'Weekly':
        data = CommitData.objects.filter(repository=repo).annotate(truncated_date=TruncWeek('date')).values('date').annotate(commit_count=Count('id'))
    elif frequency == 'Monthly':
        data =  CommitData.objects.filter(repository=repo).annotate(truncated_date=TruncMonth('date')).values('date').annotate(commit_count=Count('id'))

    context = {
        'repo': repo,
        'frequency': frequency,
        'repo_id': repo_id,
        'data': serialize('json', CommitData.objects.all())
    }

    return render(request, 'github_analytics/commit_frequency.html', context=context)


def visualize_pull_requests(request, repo_id):
    repo = get_object_or_404(Repository, github_repo_id=repo_id)
    pr_data = PullRequestData.objects.filter(repository=repo)
    print(serialize('json', PullRequestData.objects.all()))
    created_data = defaultdict(int)
    merged_data = defaultdict(int)

    for pr in pr_data:
        created_data[pr.date_created] += 1
        if pr.date_merged:
            merged_data[pr.date_merged] += 1

    created_dates = list(created_data.keys())
    created_counts = list(created_data.values())
    merged_dates = list(merged_data.keys())
    merged_counts = list(merged_data.values())

    created_trace = go.Scatter(x=created_dates, y=created_counts, mode='lines+markers', name='Created PRs')
    merged_trace = go.Scatter(x=merged_dates, y=merged_counts, mode='lines+markers', name='Merged PRs')

    layout = go.Layout(title=f'Pull Requests over time for {repo.name}', xaxis=dict(title='Date'), yaxis=dict(title='Number of PRs'))
    fig = go.Figure(data=[created_trace, merged_trace], layout=layout)
    plot_div = pyo.plot(fig, output_type='div', include_plotlyjs=False)
    
    context = {
        'repo': repo,
        'plot_div': plot_div,
        'data': serialize('json', PullRequestData.objects.all())
    }

    return render(request, 'github_analytics/visualize_pull_requests.html', context=context)

def calculate_avg_resolution_time_for_all_repos():
    # Get all repositories
    all_repos = Repository.objects.all()
    repo_names = []
    avg_times = []

    for repo in all_repos:
        # Get all closed issues for the current repository
        closed_issues = IssueData.objects.filter(repository=repo, status="closed", date_closed__isnull=False)
        
        # Calculate resolution time for each issue
        total_resolution_time = timedelta()
        for issue in closed_issues:
            resolution_time = issue.date_closed - issue.date_created
            total_resolution_time += resolution_time

        avg_time = total_resolution_time.total_seconds() / (len(closed_issues)*86400) if closed_issues else 0  # Convert to days

        repo_names.append(repo.name)
        avg_times.append(avg_time)

    return repo_names, avg_times

def visualize_all_repos_avg_resolution_time(request):
    repo_names, avg_times = calculate_avg_resolution_time_for_all_repos()

    data = [go.Bar(x=repo_names, y=avg_times)]
    layout = go.Layout(title='Average Resolution Time for Issues Across Repositories')
    fig = go.Figure(data=data, layout=layout)

    plot_div = pyo.plot(fig, output_type='div', include_plotlyjs=False)

    context = {
        'plot_div': plot_div,
    }

    return render(request, 'github_analytics/all_repos_avg_resolution_time.html', context=context)

def visualize_contributors(request, repo_id):
    repo = get_object_or_404(Repository, github_repo_id=repo_id)
    contributors_data = ContributorData.objects.filter(repository=repo)

    # Data for the plot
    names = [data.contributor.github_username for data in contributors_data]
    contribution_counts = [data.contributions_count for data in contributors_data]

    # Using Plotly to generate the bar chart
    data = [go.Bar(x=names, y=contribution_counts)]
    layout = go.Layout(title='Contributions by Contributors')
    fig = go.Figure(data=data, layout=layout)

    plot_div = pyo.plot(fig, output_type='div', include_plotlyjs=False)

    context = {
        'repo': repo,
        'plot_div': plot_div,
        'data': serialize('json', Repository.objects.all())
    }

    return render(request, 'github_analytics/visualize_contributors.html', context=context)