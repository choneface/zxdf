import tempfile
from typing import List

from rich.console import Console
from rich.panel import Panel

from zxdf.utils import clone, toGithub
from zxdf.storage import fetchSkillMetadata, saveSkillMetadata
from zxdf.services.tool_manager import findTools, moveSkillIntoAllTools, moveSkillIntoToolSkills
from zxdf.view.step import Step
from zxdf.view.symbols import SYMBOL_ARROW, SYMBOL_OK

def atLeast(x, minimium): 
    return max(x, minimium)

def addSkill(console: Console, skill: str): 
    repo = toGithub(skill)
    tools = findTools()
    commandString =f"zxdf skill [blue]add[/blue] {skill}\n" 
    toolsString = "Tools: "
    for tool in tools: 
        toolsString+= tool + ", "
    toolsString = toolsString[:-2]

    padding_right = max(64 - max(len(commandString), len(toolsString)), 0)

    infoPanel = Panel(
        commandString + toolsString,
        expand=False,
        padding=(0, padding_right, 0, 0),
    )
    console.print(infoPanel)
    console.print("")

    console.print("Resolving skill source...")
    console.print(f"{SYMBOL_OK} Resolved {skill} {SYMBOL_ARROW} {repo}\n")

    step = Step(console, "Fetching...")
    name = generateSkillName(skill)
    with tempfile.TemporaryDirectory() as temp_dir: 

        skillLocation = step.addSpinner("Cloning repository...", lambda: clone(repo, temp_dir, name))
        step.addSpinner("Adding skills to tool...", lambda: moveSkillIntoAllTools(tools, skillLocation))

        metadata = {
                "skill_name": name,
                "repository": repo,
                "tools": tools
        }
        step.addSpinner("Wrapping up...", lambda: saveSkillMetadata(metadata))

    rows = [{
        "skill": name,
        "action": "ADD",
        "tools": ",".join(tools),
        "notes": f"added as {name}"
        }]
    step.ok(rows)

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
