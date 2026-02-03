from pathlib import Path
import os, shutil
from zxdf.filesys import makeDirectory, copyFiles

home_directory = Path.home()
TOOLS = ["claude"]
TOOL_INFO = {
        "claude": {
            "root-location": home_directory / ".claude",
            "skill-location": home_directory / ".claude/skills"
        }
}

def findTools(): 
    ret = []
    for tool in TOOLS:
        info = TOOL_INFO[tool] 
        root_location = info["root-location"]
        if root_location.exists():
            ret.append(tool)
    return ret


def moveSkillIntoToolSkills(tempSkillDirectory: str, tool: str):
    skillsDirectory = TOOL_INFO[tool]["skill-location"]
    if not skillsDirectory.exists():
        os.mkdir(skillsDirectory)

    dest = skillsDirectory / Path(tempSkillDirectory).name
    shutil.copytree(tempSkillDirectory, dest)
