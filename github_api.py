import requests
import os

# Replace with your actual values
REPO = "ankitanand200193/Graded-Project-on-Building-CI-CD-Pipeline-Tool"
BRANCH = "main"
HASH_FILE = "/home/ubuntu/last_commit.txt"

# Get GitHub token from environment variable
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
if not GITHUB_TOKEN:
    print("❌ GitHub token not found. Set it in /etc/ci_env.")
    exit(1)

# GitHub API headers
headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

# GitHub API URL to get the latest commit on the branch
url = f"https://api.github.com/repos/{REPO}/commits/{BRANCH}"

try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()
except requests.exceptions.RequestException as e:
    print(f"❌ Failed to fetch commit info: {e}")
    exit(1)

latest_commit = response.json()["sha"]

# Read previously saved commit hash
if os.path.exists(HASH_FILE):
    with open(HASH_FILE, "r") as f:
        last_commit = f.read().strip()
else:
    last_commit = ""

# Compare and deploy if needed
if latest_commit != last_commit:
    print("✅ New commit found! Deploying...")
    os.system("/home/ubuntu/deploy.sh")  # Call your bash deploy script
    with open(HASH_FILE, "w") as f:
        f.write(latest_commit)
else:
    print("🔁 No new commits. Everything is up to date.")

