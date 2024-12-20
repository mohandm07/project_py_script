import os
import requests
import boto3

# GitHub Token from environment variable (GitHub secret)
GITHUB_TOKEN = os.getenv('MY_GITHUB_TOKEN')  # Use your custom secret name here

# GitHub API endpoint for listing repositories
repos_url = 'https://api.github.com/users/{username}/repos'

# Replace 'username' with the GitHub username or organization
username = 'mohandm07'  # Replace with the GitHub username or organization

# EC2 Client setup
def list_running_ec2_instances():
    # Create an EC2 client
    ec2_client = boto3.client('ec2')

    try:
        # Retrieve EC2 instance details
        response = ec2_client.describe_instances(
            Filters=[{'Name': 'instance-state-name', 'Values': ['running']}]
        )
        
        running_instances = []
        
        # Extract details from the response
        for reservation in response.get('Reservations', []):
            for instance in reservation.get('Instances', []):
                instance_details = {
                    'InstanceId': instance['InstanceId'],
                    'InstanceType': instance['InstanceType'],
                    'LaunchTime': instance['LaunchTime'],
                    'PublicIpAddress': instance.get('PublicIpAddress'),
                    'PrivateIpAddress': instance.get('PrivateIpAddress'),
                    'State': instance['State']['Name'],
                    'AvailabilityZone': instance['Placement']['AvailabilityZone'],
                    'Tags': instance.get('Tags', [])
                }
                running_instances.append(instance_details)
        
        # Display instance details
        for instance in running_instances:
            print("Instance ID:", instance['InstanceId'])
            print("Instance Type:", instance['InstanceType'])
            print("Launch Time:", instance['LaunchTime'])
            print("Public IP Address:", instance.get('PublicIpAddress'))
            print("Private IP Address:", instance.get('PrivateIpAddress'))
            print("State:", instance['State'])
            print("Availability Zone:", instance['AvailabilityZone'])
            print("Tags:", instance['Tags'])
            print("-" * 40)

        if not running_instances:
            print("No running EC2 instances found.")
    
    except Exception as e:
        print(f"Error: {e}")

# GitHub API call
def list_github_repositories():
    # Construct the full URL for GitHub API
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

# Main function to execute both tasks
if __name__ == "__main__":
    print("Listing running EC2 instances...")
    list_running_ec2_instances()
    print("\nFetching GitHub repositories...")
    list_github_repositories()
