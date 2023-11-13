"""
URL configuration for github_analytics_dashboard project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from github_analytics import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('fetch_github_data/', views.fetch_github_data, name='fetch_github_data'),
    path('', views.home, name='home'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('test/', views.test, name='test'),
    path('commit_frequency/<int:repo_id>', views.commit_frequency, name='commit_frequency'),
    path('visualize_pull_requests/<int:repo_id>', views.visualize_pull_requests, name='visualize_pull_requests'),
    path('visualize_contributors/<int:repo_id>', views.visualize_contributors, name='visualize_contributors'),
    path('visualize_repositories/', views.visualize_repositories, name='visualize_repositories'),
    path('all_repos_avg_resolution_time/', views.visualize_all_repos_avg_resolution_time, name='visualize_all_repos_avg_resolution_time'),
]
