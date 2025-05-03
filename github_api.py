import os
import requests
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

# Read the token
token = os.getenv("GITHUB_TOKEN")

headers = {
    "Authorization": f"token {token}"
}

# Configuration
owner = "ankitanand200193"    # GitHub username or organization
repo = "Graded-Project-on-Building-CI-CD-Pipeline-Tool" # Repository name
branch = "main"      # Branch name, usually 'main' or 'master'


# GitHub API URL
url = f"https://api.github.com/repos/{owner}/{repo}/commits/{branch}"

def get_latest_commit():
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        commit_data = response.json()
        print("✅ Script is working!")
        print("Latest Commit SHA:", commit_data['sha'])
        print("Commit Message:", commit_data['commit']['message'])
        print("Committed at:", commit_data['commit']['committer']['date'])
    else:
        print(f"❌ Failed. Status Code: {response.status_code}")
        print("Response:", response.text)

if __name__ == "__main__":
    get_latest_commit()