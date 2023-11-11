import requests

BASE_URL = "https://api.github.com/"

def get_headers(user_token):
    return {
        "Authorization": f"token {user_token}",
        "Accept": "application/vnd.github.v3+json"
    }

def get_user_repos(user_token):
    url = f"{BASE_URL}user/repos"
    response = requests.get(url, headers=get_headers(user_token))
    return response.json()

def get_repo_commits(user_token, repo_name):
    url = f"{BASE_URL}repos/{repo_name}/commits"
    response = requests.get(url, headers=get_headers(user_token))
    return response.json()


#def get_repo(user_token, repo_name):
#    url = f"{BASE_URL}repos/{repo_name}/REPO"
#    response = requests.get(url, headers=get_headers(user_token))
#    #print(response.json())
#    return response.json()
#

def get_repo_pull_requests(user_token, repo_name):
    url = f"{BASE_URL}repos/{repo_name}/pulls?state=all"
    response = requests.get(url, headers=get_headers(user_token))
    return response.json()

def get_repo_issues(user_token, repo_name):
    url = f"{BASE_URL}repos/{repo_name}/issues?state=all"
    response = requests.get(url, headers=get_headers(user_token))
    return response.json()

def get_repo_contributors(user_token, repo_name):
    url = f"{BASE_URL}repos/{repo_name}/contributors"
    response = requests.get(url, headers=get_headers(user_token))
    return response.json()