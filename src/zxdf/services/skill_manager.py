import tempfile
from typing import List

from rich.console import Console
from rich.panel import Panel

from zxdf.utils import clone, toGithub
from zxdf.storage import fetchSkillMetadata, saveSkillMetadata
from zxdf.services.tool_manager import findTools, moveSkillIntoAllTools, moveSkillIntoToolSkills
from zxdf.view.action import Action
from zxdf.view.symbols import SYMBOL_ARROW

def atLeast(x, minimium): 
    return max(x, minimium)

def addSkill(console: Console, skill: str): 
    repo = toGithub(skill)
    tools = findTools()
    commandString =f"zxdf skill [blue]add[/blue] {skill}\n" 
    infoPanel = _addCommandInfoPanel(commandString, tools)

    action = Action(console)
    action.header(infoPanel)

    action.info("Resolving skill source...")
    action.okLine(f"Resolved {skill} {SYMBOL_ARROW} {repo}\n")

    action.info("Fetching...")
    name = generateSkillName(skill)
    with tempfile.TemporaryDirectory() as temp_dir: 

        skillLocation = action.addSpinner("Cloning repository...", lambda: clone(repo, temp_dir, name))
        action.addSpinner("Adding skill to tool...", lambda: moveSkillIntoAllTools(tools, skillLocation))

        metadata = {
                "skill_name": name,
                "repository": repo,
                "tools": tools
        }
        action.addSpinner("Wrapping up...", lambda: saveSkillMetadata(metadata))

    rows = [{
        "skill": skill,
        "action": "ADD",
        "tools": ",".join(tools),
        "notes": f"added as {name}"
        }]
    action.ok(rows)

def getAllSkills() -> List:
    skills = fetchSkillMetadata()
    deduped = list({s["skill_name"] for s in skills})
    ordered = sorted(deduped) 
    return ordered

def updateSkills(console: Console, skills: List, verify: bool, updateAll: bool):
    if len(skills) == 1:
        commandString = f"zxdf skill [blue]update[/blue] {skills[0]}\n"
    else:
        commandString = f"zxdf skill [blue]update[/blue] {skills[0]} and [pink]{len(skills) - 1}[/pink] more\n"

    flagsString = f"Verify: [blue]{ 'yes' if verify else 'no' }[/blue]    Update All: [blue]{ 'yes' if updateAll else 'no' }[/blue]"

    infoPanel = _updateCommandInfoPanel(commandString, flagsString)
    action = Action(console)
    action.header(infoPanel)
    all_metadata = fetchSkillMetadata()
    summary_rows = []

    action.info("Fetching...")
    for skill in skills:
        skill_meta = None
        for meta in all_metadata:
            if meta["skill_name"] == skill:
                skill_meta = meta
                break

        row = {
            "skill": skill,
            "action": "UPDATE",
            "notes": "up-to-date"
            }

        if skill_meta is None:
            row["tools"] = ""
            row["notes"] = "not found in metadata"
            summary_rows.append(row)
            continue
        
        row["tools"] = ",".join(skill_meta["tools"])

        try:
            action.addSpinner(f"Updating {skill}...", lambda: _updateSkillsAcrossTools(skill_meta))
        except Exception:
            row["notes"] = "failed to pull from remote"

        summary_rows.append(row)

    action.ok(summary_rows)


def generateSkillName(skill: str) -> str:
    return skill.replace("/", "@")

def _updateSkillsAcrossTools(skill_meta):
    skill = skill_meta["skill_name"]
    repo = skill_meta["repository"]
    tools = skill_meta["tools"]
    with tempfile.TemporaryDirectory() as temp_dir:
        skill_location = clone(repo, temp_dir, skill)
        for tool in tools:
            moveSkillIntoToolSkills(str(skill_location), tool)

def _updateCommandInfoPanel(commandString, flagsString):
    padding_right = max(72- max(len(commandString), len(flagsString)), 0)
    return Panel(
        commandString + flagsString,
        expand=False,
        padding=(0, padding_right, 0, 0),
    )


def _addCommandInfoPanel(commandString, tools):
    toolsString = "Tools: " + ",".join(tools)

    padding_right = max(64 - max(len(commandString), len(toolsString)), 0)

    return Panel(
        commandString + toolsString,
        expand=False,
        padding=(0, padding_right, 0, 0),
    )
