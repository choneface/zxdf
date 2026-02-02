import subprocess
from pathlib import Path

def copyFiles(src: str, dest: str):
    subprocess.run(["cp", "-r", src, dest])

def makeDirectory(directory: Path):
    subprocess.run(["mkdir", str(directory)])
