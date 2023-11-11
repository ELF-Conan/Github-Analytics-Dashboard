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

#from github.models import Repository, Commit
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
        with open('./commit.json', 'w') as file1:
            json.dump(commits, file1)
        ###commit_count_by_date = defaultdict(int)
        ###for commit in commits:
        ###    commit_date_str = commit["commit"]["author"]["date"]
        ###    commit_date = datetime.strptime(commit_date_str, "%Y-%m-%dT%H:%M:%SZ").date()
        ###    commit_count_by_date[commit_date] += 1
        for commit in commits:
            commit_date = datetime.strptime(commit['commit']['author']['date'], '%Y-%m-%dT%H:%M:%SZ').date()

        #for date, count in commit_count_by_date.items():
            CommitData.objects.get_or_create(
                repository=repo_obj,
                date=commit_date,
        #        defaults={"commit_count": count},   
            )
        print(serialize('json', CommitData.objects.all()))
        with open('./commit.json', 'w') as file2:
            json.dump(commits, file2)
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
        #with open('./contributors.json', 'w') as file2:
        #    json.dump(contributors, file2)
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
    #raw_date = CommitData.objects.values('date')
    # print("I am raw date: " + json.dumps(raw_date))
    if frequency == 'Daily':
        # For daily, we can use the data as it is
        #commits_data = CommitData.objects.filter(repository=repo)
        #dates = [commit.date for commit in commits_data]
        #counts = [commit.commit_count for commit in commits_data]
        #print(serialize('json', CommitData.objects.all()))
        #data =  CommitData.objects.filter(repository=repo).annotate(truncated_date=TruncDay('date')).values('date').annotate(commit_count=Count('id'))
        
        data = CommitData.objects.annotate(commit_count=Count('date'))
    elif frequency == 'Weekly':
        # You'll have to aggregate the data on a weekly basis. This is just a simple example and may require adjustments.
        #commits_data = CommitData.objects.filter(repository=repo).extra(select={'week': 'date(date_trunc(\'week\', date))'}).values('week').annotate(total=Sum('commit_count'))
        #dates = [commit['week'] for commit in commits_data]
        #counts = [commit['total'] for commit in commits_data]
        data = CommitData.objects.filter(repository=repo).annotate(truncated_date=TruncWeek('date')).values('date').annotate(commit_count=Count('id'))
    elif frequency == 'Monthly':
        # Similar to weekly, but for month
        #commits_data = CommitData.objects.filter(repository=repo).extra(select={'month': 'date(date_trunc(\'month\', date))'}).values('month').annotate(total=Sum('commit_count'))
        #dates = [commit['month'] for commit in commits_data]
        #counts = [commit['total'] for commit in commits_data]
        data =  CommitData.objects.filter(repository=repo).annotate(truncated_date=TruncMonth('date')).values('date').annotate(commit_count=Count('id'))

    # dates = [item['date'] for item in data]
    # counts = [item['commit_count'] for item in data]
    #print('jjjjjjjjjbbbb')
    #print(data)
    #print(dates)
    #print(counts)
    #plt.figure(figsize=(10, 6))
    #plt.plot(dates, counts, marker='o')
    #plt.title(f'Commit Frequency for {repo.name} ({frequency})')
    #plt.xlabel('Date')
    #plt.ylabel('Number of Commits')
    #plt.grid(True)
    #plot_dir = 'github_analytics'
    #plot_path = os.path.join(plot_dir, f'commit_frequency_{frequency}.png')
    #plt.savefig(plot_path)
    #plt.close()
    # Assuming Commit model has fields 'date' and 'count'

    # Using Plotly to generate the chart
    #data = [go.Bar(x=dates, y=counts)]
    #layout = go.Layout(title=f'Commit Frequency Over Time ({frequency})')
    #fig = go.Figure(data=data, layout=layout)
    #title=f'Commit Frequency Over Time ({frequency})'
    # fig = px.line(x=dates, y=counts, labels={'x': 'Date', 'y': 'Number of Commits'}, title=title)
    #plot_div = pyo.plot(fig, output_type='div', include_plotlyjs=False)

    context = {
        'repo': repo,
        #'plot_div': plot_div,
        # 'plot_div': fig.to_html(full_html=False),
        'frequency': frequency,
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