import subprocess

def git_add(paths):
    subprocess.run(["git", "add"] + paths, check=True)

def git_commit(message):
    subprocess.run(["git", "commit", "-m", message], check=True)

def git_push():
    subprocess.run(["git", "push"], check=True)

def commit_episode(title, files, commit=True, push=True):
    if not commit:
        return
    
    git_add(files)
    git_commit(f"Add episode: {title}")
    
    if push:
        git_push()
