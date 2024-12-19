import os
import requests

# GitHub Token from environment variable (GitHub secret)
GITHUB_TOKEN = os.getenv('MY_GITHUB_TOKEN')  # Use your custom secret name here

# GitHub API endpoint for listing repositories
repos_url = 'https://api.github.com/users/{username}/repos'

# Replace 'username' with the GitHub username or organization
username = 'mohandm07'  # Replace with the GitHub username or organization

# Construct the full URL
url = repos_url.format(username=username)

# Set up headers for the request with authentication
headers = {
    'Authorization': f'token {GITHUB_TOKEN}',
    'Accept': 'application/vnd.github.v3+json',
}

# Make the GET request to the GitHub API
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    repos = response.json()
    print(f"Repositories for {username}:")
    for repo in repos:
        print(f"Name: {repo['name']}, Description: {repo.get('description', 'No description')}, Stars: {repo['stargazers_count']}")
else:
    print(f"Error: {response.status_code} - {response.text}")
