import tempfile
import subprocess

def addSkill(skill: str): 
    repo = "git@github.com:" + skill + ".git"
    print(f"fetching {repo} from remote")
    with tempfile.TemporaryDirectory() as temp_dir: 
        subprocess.run(['git', 'clone', repo], cwd=temp_dir)
