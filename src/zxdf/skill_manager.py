import tempfile

from zxdf.git import clone, toGithub
from zxdf.systemfiles import saveSkillMetadata
from zxdf.tool_manager import findTools, moveSkillIntoToolSkills

def addSkill(skill: str): 
    repo = toGithub(skill)
    print(f"fetching {repo} from remote")
    with tempfile.TemporaryDirectory() as temp_dir: 
        name = generateSkillName(skill)
        skillLocation = clone(repo, temp_dir, name)

        tools = findTools()
        for tool in tools:
            print(f"installing skill for {tool}")
            moveSkillIntoToolSkills(str(skillLocation), tool)

        metadata = {
                "skill_name": name,
                "repository": repo,
                "tools": tools
        }
        saveSkillMetadata(metadata)

def generateSkillName(skill: str) -> str:
    return skill.replace("/", ":")
