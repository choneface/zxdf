from pathlib import Path

from zxdf.filesys import makeDirectory, moveFiles

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


def moveSkillIntoToolSkills(skillDirectory: str, tool: str):
    skillsDirectory = TOOL_INFO[tool]["skill-location"]
    if not skillsDirectory.exists():
        print(f"{skillsDirectory} not found, making new skills directory for {tool}")
        makeDirectory(skillsDirectory)

    moveFiles(skillDirectory, str(skillsDirectory))

