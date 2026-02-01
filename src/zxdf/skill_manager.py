import tempfile
import subprocess

from zxdf.git import clone, toGithub

def addSkill(skill: str): 
    repo = toGithub(skill)
    print(f"fetching {repo} from remote")
    with tempfile.TemporaryDirectory() as temp_dir: 
        clone(repo, temp_dir)
