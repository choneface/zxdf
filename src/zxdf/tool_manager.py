from pathlib import Path

home_directory = Path.home()
TOOLS = ["claude"]
TOOL_INFO = {
        "claude": {
            "root-location": ".claude",
            "skill-location": ".claude/skills"
        }
}

def findTools(): 
    ret = []
    for tool in TOOLS:
        info = TOOL_INFO[tool] 
        root_location = home_directory / info["root-location"]
        if root_location.exists():
            ret.append(tool)
    return ret

