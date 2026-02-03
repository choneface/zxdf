import subprocess
from pathlib import Path

def clone(repo: str, directory: str, name: str):
    subprocess.run(['git', 'clone', '--quiet', repo, name], cwd=directory, check=True)
    return Path(directory) / name

def toGithub(skill: str) -> str:
    return "https://github.com/" + skill + ".git"
