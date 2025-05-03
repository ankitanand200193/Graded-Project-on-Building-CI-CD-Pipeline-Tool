# Lightweight CI/CD Pipeline using Bash, Python, and Cron on AWS EC2

## Overview

This project demonstrates how to build a secure and lightweight CI/CD pipeline using basic tools like Bash, Python, and Cron on an AWS EC2 instance. It continuously monitors a GitHub repository for new commits and automatically deploys updated HTML content to a web server powered by Nginx.

---

## Tech Stack

| Component       | Tool Used        |
| --------------- | ---------------- |
| Version Control | Git + GitHub     |
| Web Server      | Nginx            |
| Automation      | Cron Jobs        |
| Programming     | Python + Bash    |
| Server Hosting  | AWS EC2 (Ubuntu) |
| Deployment Mode | Git Pull + Copy  |

---

## Project Architecture

```
/home/ubuntu/
│
├── check_commit.py        # Python script to check for new commits
├── deploy.sh              # Bash script to pull latest code and restart Nginx
└── /etc/ci_env            # Secure file storing GitHub token
├── last_commit.txt        # For tracking the latest deployed commit
```

---

## Setup Instructions

### 1. Create and Push HTML Project to GitHub

* Create a basic `index.html`
* Initialize Git, commit, and push to a **public** GitHub repository

### 2. Configure AWS EC2 + Nginx

* Launch Ubuntu EC2 instance
* Install Nginx: `sudo apt update && sudo apt install nginx -y && sudo apt install python3-pip -y`
* Allow HTTP in EC2 Security Group
* Default site directory: `/var/www/html`

### Creating Access Token
1. Create a GitHub Personal Access Token (classic)

    Go to: `GitHub → Settings → Developer settings → Personal access tokens`
    Generate a token with `repo` and `read-only access`.

### 3. Store GitHub Token 

Create `sudo nano /etc/ci_env`:

```bash
export GITHUB_TOKEN="ghp_your_token"
```

Secure it:

```bash
sudo chmod 600 /etc/ci_env
```

### 4. Create Python Script `check_commit.py` in the ubuntu ec2 instance

```bash
nano home/ubuntu/check_commit.py
```
Python code
```bash
import requests
import os

# Replace with your actual values
REPO = "ankitanand200193/Graded-Project-on-Building-CI-CD-Pipeline-Tool"
BRANCH = "main"
HASH_FILE = "/home/ubuntu/last_commit.txt"

# Get GitHub token from environment variable
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
if not GITHUB_TOKEN:
    print("GitHub token not found. Set it in /etc/ci_env.")
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
    print(f"Failed to fetch commit info: {e}")
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
    print("New commit found! Deploying...")
    os.system("/home/ubuntu/deploy.sh")  # Call your bash deploy script
    with open(HASH_FILE, "w") as f:
        f.write(latest_commit)
else:
    print("No new commits. Everything is up to date.")

```
* Checks GitHub API for new commits
* Calls deploy script if commit is new

#### Test the python using

```bash
sudo bash -c "source /etc/ci_env && python3 /home/ubuntu/check_commit.py"
```

### 5. Create Deployment Script `deploy.sh` in the ubuntu ec2 instance

```bash
nano home/ubuntu/deploy.sh
```
bash code

```bash
#!/bin/bash

# Config
REPO_URL="https://github.com/ankitanand200193/Graded-Project-on-Building-CI-CD-Pipeline-Tool.git"
APP_DIR="/var/www/html"

# Temp directory for clone
TMP_DIR="/tmp/site-deploy"

echo "Cloning latest code..."

# Clean up previous temp
rm -rf "$TMP_DIR"
git clone "$REPO_URL" "$TMP_DIR"

if [ $? -ne 0 ]; then
    echo "Git clone failed!"
    exit 1
fi

echo "Deploying to $APP_DIR..."

# Copy new files to web root
sudo rm -rf "$APP_DIR"/*
sudo cp -r "$TMP_DIR"/* "$APP_DIR"

# Set proper permissions
sudo chown -R www-data:www-data "$APP_DIR"

# Restart Nginx (if needed)
echo "Restarting Nginx..."
sudo systemctl reload nginx

echo "Deployment complete."

```

Make it executable:

```bash
chmod +x home/ubuntu/deploy.sh
```

* Clones repo
* Clears `/var/www/html` and copies new content
* Reloads Nginx



### 6. Setup Cron Job

Run `sudo crontab -e` and add:

```bash
*/2 * * * * bash -c "source /etc/ci_env && /usr/bin/python3 /home/ubuntu/check_commit.py >> /var/log/ci_cd.log 2>&1"
```

#### Cron logs screenshot

Screenshot?????
---

## Log Monitoring

To view live logs:

```bash
tail -f /var/log/ci_cd.log
```

---

## Testing

* Make a new commit in the GitHub repo
* Wait \~2 minutes
* Reload EC2 public IP in browser to see deployed changes

---

