# Utilities for interacting with GitHub API

import requests
import os

GITHUB_API_URL = "https://api.github.com"


def get_repositories(username, token, org=None):
    """Get all repositories for a user or org, incluindo times admin/maintainer."""
    headers = {"Authorization": f"token {token}"}
    repos = []
    page = 1
    base_url = f"{GITHUB_API_URL}/users/{username}/repos" if not org else f"{GITHUB_API_URL}/orgs/{org}/repos"
    while True:
        url = f"{base_url}?page={page}&per_page=100"
        resp = requests.get(url, headers=headers)
        if resp.status_code != 200:
            break
        data = resp.json()
        if not data:
            break
        for repo in data:
            # Buscar times do repo
            teams_url = f"{GITHUB_API_URL}/repos/{org or username}/{repo['name']}/teams"
            teams_resp = requests.get(teams_url, headers=headers)
            teams = []
            if teams_resp.status_code == 200:
                teams = teams_resp.json()
            repo['teams_admin'] = [t['name'] for t in teams if t.get('permission') == 'admin']
            repo['teams_maintainer'] = [t['name'] for t in teams if t.get('permission') == 'maintain']
            repo['teams_granular'] = [
                {'team': t['name'], 'role': t.get('permission', '')}
                for t in teams
            ]
            repos.append(repo)
        page += 1
    return repos

def download_readme(owner, repo, token, dest_folder):
    """Download README.md from a repo."""
    headers = {"Authorization": f"token {token}"}
    url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/readme"
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        content = resp.json().get('content')
        import base64
        readme = base64.b64decode(content).decode('utf-8')
        with open(os.path.join(dest_folder, f"{repo}_README.md"), "w", encoding="utf-8") as f:
            f.write(readme)
        return True
    return False
