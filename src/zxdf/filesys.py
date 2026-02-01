import subprocess
from pathlib import Path

def moveFiles(src: str, dest: str):
    subprocess.run(["mv", src, dest])

def makeDirectory(directory: Path):
    subprocess.run(["mkdir", str(directory)])
