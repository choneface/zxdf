import subprocess

def clone(repo: str, directory: str):
    subprocess.run(['git', 'clone', repo], cwd=directory)

def toGithub(skill: str) -> str:
    return "git@github.com:" + skill + ".git"
