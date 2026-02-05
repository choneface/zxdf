import tempfile
from typing import List

from rich.console import Console

from zxdf.utils import clone, toGithub
from zxdf.storage import fetchSkillMetadata, saveSkillMetadata
from zxdf.services.tool_manager import findTools, moveSkillIntoToolSkills

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
    all_metadata = fetchSkillMetadata()
    failures = []

    for skill in skills:
        # Find metadata for this skill
        skill_meta = None
        for meta in all_metadata:
            if meta["skill_name"] == skill:
                skill_meta = meta
                break

        if skill_meta is None:
            failures.append((skill, "not found in metadata"))
            continue

        repo = skill_meta["repository"]
        tools = skill_meta["tools"]

        try:
            with console.status(f"[bold green]Updating {skill}..."):
                with tempfile.TemporaryDirectory() as temp_dir:
                    skill_location = clone(repo, temp_dir, skill)

                    for tool in tools:
                        moveSkillIntoToolSkills(str(skill_location), tool)

            console.print(f"[bold green]{skill} updated")
        except Exception as e:
            failures.append((skill, str(e)))
            console.print(f"[bold red]{skill} failed to update")

    if failures:
        console.print("\n[bold red]The following updates failed:[/bold red]")
        for skill, reason in failures:
            console.print(f"  - {skill}: {reason}")

def generateSkillName(skill: str) -> str:
    return skill.replace("/", "@")
