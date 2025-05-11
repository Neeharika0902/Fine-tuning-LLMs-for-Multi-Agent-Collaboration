"""
GitHub integration utilities for the multi-agent chatbot system
"""
from datetime import datetime
import re
from github import Github
from server.config import GITHUB_TOKEN, GITHUB_REPO, GITHUB_BRANCH

def push_md_to_github_with_auto_numbering(
    github_token=GITHUB_TOKEN,
    repo_name=GITHUB_REPO,
    content="",
    commit_message="Daily Status Commits",
    folder_name=None,
    branch=GITHUB_BRANCH
):
    """
    Push markdown content to GitHub repository with auto-incremented file names (file1.md, file2.md, etc.)

    Parameters:
    github_token (str): Personal access token for GitHub
    repo_name (str): Name of the repository (format: 'username/repo')
    content (str): Content to be pushed to the markdown file
    commit_message (str): Commit message
    folder_name (str): Optional custom folder name (if None, creates date-based folder)
    branch (str): Branch to push to (default is 'main')
    
    Returns:
    str or None: The path of the created file, or None if an error occurred
    """
    try:
        # Initialize the GitHub instance with your token
        g = Github(github_token)

        # Get the repository
        repo = g.get_repo(repo_name)

        # Create folder name based on current date if not provided
        if folder_name is None:
            today = datetime.now()
            folder_name = today.strftime("%Y-%m-%d")

        # Check if folder exists and get existing files
        try:
            # Check if the folder exists by trying to get contents
            folder_contents = repo.get_contents(folder_name, ref=branch)
            print(f"Folder '{folder_name}' exists. Checking existing files...")

            # Find the highest file number
            highest_number = 0
            file_pattern = re.compile(r'file(\d+)\.md')

            for item in folder_contents:
                if item.type == "file":
                    match = file_pattern.match(item.name)
                    if match:
                        file_num = int(match.group(1))
                        highest_number = max(highest_number, file_num)

            # Create the next file number
            next_number = highest_number + 1

        except Exception as e:
            print(f"Folder '{folder_name}' doesn't exist or couldn't access contents. Creating the first file.")
            # Start with file1.md if folder doesn't exist
            next_number = 1

        # Create file name with the next sequential number
        file_name = f"file{next_number}.md"

        # Create full path for the file
        file_path = f"{folder_name}/{file_name}"

        # Create the file (this will also create the folder if needed)
        repo.create_file(
            file_path, commit_message, content, branch=branch
        )
        print(f"File '{file_path}' created successfully on GitHub!")
        return file_path

    except Exception as e:
        print(f"Error creating file: {str(e)}")
        return None
