import tempfile, shutil

from zxdf.git import clone, toGithub
from zxdf.systemfiles import saveSkillMetadata
from zxdf.tool_manager import findTools, moveSkillIntoToolSkills

def addSkill(skill: str): 
    repo = toGithub(skill)
    with tempfile.TemporaryDirectory() as temp_dir: 
        name = generateSkillName(skill)
        skillLocation = clone(repo, temp_dir, name)

        tools = findTools()
        for tool in tools:
            moveSkillIntoToolSkills(str(skillLocation), tool)

        metadata = {
                "skill_name": name,
                "repository": repo,
                "tools": tools
        }
        saveSkillMetadata(metadata)

def generateSkillName(skill: str) -> str:
    return skill.replace("/", "@")
