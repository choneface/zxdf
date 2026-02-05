from typing import Annotated, List

import typer
from rich.console import Console

from zxdf.skill_manager import addSkill, getAllSkills, updateSkills
from zxdf.skill_picker import confirm, skillPicker

skill_app = typer.Typer(help="Manage AI skills")
console = Console()


@skill_app.command()
def add(skill: Annotated[str, typer.Argument(help="[bold]format: author/skillname")]):
    """Add a skill by providing skill slug."""
    with console.status("[bold green]Adding skill..."):
        addSkill(skill)
    console.print("[bold green]Skill added")


@skill_app.command()
def update(
    skill: Annotated[
        str,
        typer.Argument(help="[bold]format: author/skillname or leave empty to launch skill picker"),
    ] = "",
    update_all: Annotated[
        bool,
        typer.Option(help="[bold]indicates all skills should be updated"),
    ] = False,
    verify: Annotated[
        bool,
        typer.Option(help="[bold]indicates whether CLI should verify your choice before execution"),
    ] = True,
):
    """Update a skill by providing its slug or update all by running without skill slug."""
    skills_to_update: List[str]

    if update_all:
        skills_to_update = getAllSkills()
    elif skill == "":
        skills_to_update = skillPicker(console, getAllSkills())
    else:
        skills_to_update = [skill]

    if not skills_to_update:
        return

    if verify:
        confirmed = confirm(
            console, "Are you sure you want to update the following skills?", skills_to_update
        )
        if not confirmed:
            console.print("No worries, exiting")
            return

    updateSkills(console, skills_to_update)
