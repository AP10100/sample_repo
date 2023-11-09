import requests

# GitHub API endpoint to get repositories
github_api_url = 'https://spruce.arlo.com/api/v3/user/repos'

# Your GitHub personal access token
github_token = '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'

# Request headers
headers = {
    'Authorization': f'token {github_token}'
}

# Make the request to get repositories
response = requests.get(github_api_url, headers=headers)

if response.status_code == 200:
    repos = response.json()
    with open('github_repos_and_branches.txt', 'w') as file:
        for repo in repos:
            repo_name = repo['full_name']
            branches_url = f'https://spruce.arlo.com/api/v3/repos/{repo_name}/branches'
            branches_response = requests.get(branches_url, headers=headers)
            if branches_response.status_code == 200:
                branches = branches_response.json()
                branch_names = [branch['name'] for branch in branches]
                file.write(f'Repo: {repo_name}\n')
                file.write(f'Branches: {", ".join(branch_names)}\n\n')
else:
    print(f'Error connecting to GitHub API. Status code: {response.status_code}')


# -----------------------------------------------------------------------------------------------

jenkins_url = "https://cicdxc.arlocloud.com/"
api_token = "111a78a4b320267b90f5c4ff96044ac134"  # Replace with your Jenkins API token


# Request headers for basic authentication
headers = {
    'Content-Type': 'application/xml',
    'Authorization': f'Bearer {api_token}'
}

# Get a list of all jobs
response = requests.get(f'{jenkins_url}/api/json', headers=headers)

if response.status_code == 200:
    data = response.json()
    multibranch_jobs = [job['name'] for job in data['jobs'] if 'multibranch' in job['_class'].lower()]

    with open('jenkins_jobs_and_branches.txt', 'w') as file:
        for job_name in multibranch_jobs:
            job_response = requests.get(f'{jenkins_url}/job/{job_name}/api/json', headers=headers)
            if job_response.status_code == 200:
                job_data = job_response.json()
                file.write(f'Job: {job_name}\n')
                file.write(f'Branches:\n')
                for branch in job_data['jobs']:
                    branch_name = branch['name']
                    file.write(f'  - {branch_name}\n')
                file.write('\n')
            else:
                print(f'Error fetching branches for {job_name}. Status code: {job_response.status_code}')

else:
    print(f'Error connecting to Jenkins API. Status code: {response.status_code}')


# ------------------------------------------------------------------------------------------

# This will list the Deleted branches in deleted_branches.txt file
# Read content of both files
with open('jenkins_jobs_and_branches.txt', 'r') as jenkins_file, open('github_repos_and_branches.txt', 'r') as github_file:
    jenkins_content = jenkins_file.read()
    github_content = github_file.read()

# Extract branches from Jenkins content
jenkins_branches = set()
current_job = None
for line in jenkins_content.split('\n'):
    if line.startswith('Job: '):
        current_job = line.split('Job: ')[1]
    elif line.startswith('  - ') and current_job is not None:
        jenkins_branches.add(line.split('  - ')[1])

# Extract branches from GitHub content
github_branches = set()
for line in github_content.split('\n'):
    if line.startswith('Branches: '):
        github_branches.update(branch.strip() for branch in line.split('Branches: ')[1].split(', '))

# Identify deleted branches
deleted_branches = jenkins_branches - github_branches

# Write the deleted branches to a file
with open('deleted_branches.txt', 'w') as deleted_file:
    deleted_file.write("List of Jenkins branches not found in GitHub:\n\n")
    for branch in deleted_branches:
        deleted_file.write(f'Branch Name: {branch}\n')
        
        
# ------------------------------------------------------------------------------------------------------------------------


# This will list the deleted Branches with the deleted Job and store it to deleted_branches_with_jobs.txt file
# Read content of both files
with open('deleted_branches.txt', 'r') as delete_file, open('jenkins_jobs_and_branches.txt', 'r') as jenkins_file:
    delete_content = delete_file.read()
    jenkins_content = jenkins_file.read()

# Extract branch names from delete content
deleted_branches = set()
for line in delete_content.split('\n'):
    if line.startswith('Branch Name: '):
        branch_name = line.split('Branch Name: ')[1]
        deleted_branches.add(branch_name)

# Extract job names and branches from Jenkins content
job_branch_mapping = {}
current_job = None
for line in jenkins_content.split('\n'):
    if line.startswith('Job: '):
        current_job = line.split('Job: ')[1]
    elif line.startswith('  - ') and current_job is not None:
        branch_name = line.split('  - ')[1]
        if branch_name not in job_branch_mapping:
            job_branch_mapping[branch_name] = []
        job_branch_mapping[branch_name].append(current_job)

# Identify deleted branches and their corresponding jobs
deleted_branches_with_jobs = {}
for branch in deleted_branches:
    if branch in job_branch_mapping:
        deleted_branches_with_jobs[branch] = job_branch_mapping[branch]

# Write the deleted branches with corresponding jobs to a file
with open('deleted_branches_with_jobs.txt', 'w') as deleted_file:
    deleted_file.write("List of Jenkins branches not found in GitHub with corresponding jobs:\n\n")
    for branch, jobs in deleted_branches_with_jobs.items():
        deleted_file.write(f'Branch Name: {branch}, Job Names: {", ".join(jobs)}\n')


# -----------------------------------------------------------------------------------------------------------------------------


#  finding the common branches in both Jenkins and Github and store it to Common...txt file
# Read the content of jenkins_jobs_and_branches.txt
with open('jenkins_jobs_and_branches.txt', 'r') as file:
    jenkins_content = file.read()

# Read the content of github_repos_and_branches.txt
with open('github_repos_and_branches.txt', 'r') as file:
    github_content = file.read()

# Extract branches and associated jobs from jenkins_content
jenkins_jobs = {}
current_job = None
for line in jenkins_content.splitlines():
    if line.startswith('Job:'):
        current_job = line.split('Job:')[1].strip()
        jenkins_jobs[current_job] = []
    elif line.startswith('  - '):
        jenkins_jobs[current_job].append(line.strip().replace('- ', ''))

# Extract branches from github_content
github_branches = set()
for line in github_content.splitlines():
    if line.startswith('Branches:'):
        github_branches.update(line.strip().split(':')[1].strip().split(', '))

# Find common branches and associated jobs
common_branches = {}
for job, branches in jenkins_jobs.items():
    common = set(branches).intersection(github_branches)
    if common:
        common_branches[job] = common

# Write common branches and associated jobs to a new Python file
with open('common_branches_and_jobs.txt', 'w') as file:
    for job, branches in common_branches.items():
        file.write(f'Job: {job}\n')
        file.write('Branches:\n')
        for branch in branches:
            file.write(f'  - {branch}\n')
        file.write('\n')


#--------------------------------------------------------------------------------------------------------------------

import csv

# Read the content of deleted_branches_with_jobs.txt
with open('deleted_branches_with_jobs.txt', 'r') as file:
    content = file.readlines()

# Extract branch names and job names
data = []
for line in content:
    if line.startswith('Branch Name:'):
        branch = line.split(',')[0].split(': ')[1].strip()
        jobs = line.split(',')[1].split(': ')[1].strip().split(', ')
        data.append([branch, ', '.join(jobs)])

# Write to CSV
with open('deleted_branches_with_jobs.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Branch Name', 'Job Names'])
    writer.writerows(data)

print('CSV file created successfully.')

