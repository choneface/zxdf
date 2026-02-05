from typing import Annotated
from rich.console import Console
import typer

from zxdf.skill_manager import addSkill, getAllSkills, updateSkills
from zxdf.skill_picker import skillPicker, confirm

app = typer.Typer(help="CLI tool for managing AI skills. Interact with the CLI using skill slugs (author/skillname)")
skills_app = typer.Typer()
tools_app = typer.Typer()

app.add_typer(skills_app, name="skill")
app.add_typer(tools_app, name="tool")

console = Console()

@skills_app.command()
def add(skill: Annotated[str, typer.Argument(help="[bold]format: author/skillname")]):
    """
    Add skill by providing skill slug
    """
    with console.status("[bold green]Adding skill..."):
        addSkill(skill)
    console.print("[bold green]Skill added")


@skills_app.command()
def update(
        skill: Annotated[str, typer.Argument(help="[bold]format: author/skillname or leave empty to launch skill picker")] = "",
        update_all: Annotated[bool, typer.Option(help="[bold]indicates all skills should be updated")] = False,
        verify: Annotated[bool, typer.Option(help="[bold]indicates whether CLI should verify your choice before execution")] = True
):
    """
    Update a skill by providing its slug or update all by running without skill slug
    """
    if update_all:
        skills_to_update = getAllSkills()
    elif skill == "":
        skills_to_update = skillPicker(console, getAllSkills())
    else:
        skills_to_update = [skill]

    if not skills_to_update:
        return

    if verify:
        confirmed = confirm(console, "Are you sure you want to update the following skills?", skills_to_update)
        if not confirmed:
            console.print("No worries, exiting")
            return

    updateSkills(console, skills_to_update)


if __name__ == "__main__":
    app()
