import tempfile
from time import sleep
from typing import List

from rich.console import Console

from zxdf.git import clone, toGithub
from zxdf.systemfiles import fetchSkillMetadata, saveSkillMetadata
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

def getAllSkills() -> List:
    skills = fetchSkillMetadata()
    deduped = list({s["skill_name"] for s in skills})
    ordered = sorted(deduped) 
    return ordered

def updateSkills(console: Console, skills: List):
    for skill in skills: 
        with console.status(f"[bold green]Updating {skill}...") as status:
            sleep(5)
        console.print(f"[bold green]{skill} updated")

    
     

def generateSkillName(skill: str) -> str:
    return skill.replace("/", "@")
