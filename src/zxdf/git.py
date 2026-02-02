import subprocess
from pathlib import Path

from zxdf.filesys import makeDirectory

def clone(repo: str, directory: str, name: str):
    subprocess.run(['git', 'clone', repo, name], cwd=directory)
    return Path(directory + "/" + name)

def toGithub(skill: str) -> str:
    return "git@github.com:" + skill + ".git"
