import tempfile
import subprocess

from zxdf.git import clone, toGithub
from zxdf.tool_manager import findTools

def addSkill(skill: str): 
    repo = toGithub(skill)
    print(f"fetching {repo} from remote")
    with tempfile.TemporaryDirectory() as temp_dir: 
        clone(repo, temp_dir)

        tools = findTools()
        for tool in tools:
            print(f"installing skill for {tool}")
