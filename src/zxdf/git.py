import subprocess
from pathlib import Path

_ssh_configured = None

def hasSSHConfigured() -> bool:
    global _ssh_configured
    if _ssh_configured is not None:
        return _ssh_configured

    try:
        result = subprocess.run(
            ['ssh', '-T', '-o', 'StrictHostKeyChecking=accept-new', '-o', 'BatchMode=yes', 'git@github.com'],
            capture_output=True,
            text=True,
            timeout=10
        )
        # GitHub returns exit code 1 with "successfully authenticated" message
        # Exit code 255 means connection failed
        _ssh_configured = result.returncode == 1
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        _ssh_configured = False

    return _ssh_configured

def clone(repo: str, directory: str, name: str):
    subprocess.run(['git', 'clone', '--quiet', repo, name], cwd=directory, check=True)
    return Path(directory) / name

def toGithub(skill: str) -> str:
    if hasSSHConfigured():
        return "git@github.com:" + skill + ".git"
    return "https://github.com/" + skill + ".git"
