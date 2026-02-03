from typing import Annotated
from rich.console import Console
import typer

from zxdf.skill_manager import addSkill, getAllSkills
from zxdf.skill_picker import skillPicker

app = typer.Typer(help="CLI tool for managing AI skills. Interact with the CLI using skill slugs (author/skillname)")
console = Console()

@app.command()
def add(skill: Annotated[str, typer.Argument(help="[bold]format: author/skillname")]):
    """
    Add skill by providing skill slug
    """
    with console.status("[bold green]Adding skill...") as status:
        addSkill(skill)
    console.print("[bold green]Skill added")


@app.command()
def update(
        skill: Annotated[str, typer.Argument(help="[bold]format: author/skillname or leave empty to launch skill picker")] = "",
        update_all: Annotated[bool, typer.Option(help="[bold]indicates all skills should be updated")] = False,
        verify: Annotated[bool, typer.Option(help="[bold]indicates whether CLI should verify your choice before execution")] = True
):
    """
    Update a skill by providing its slug or update all by running without skill slug
    """
    skillsToBeUpdated = []
    if update_all: 
        skillsToBeUpdated = getAllSkills()
    elif skill == "":
        skillsToBeUpdated = skillPicker(console)
    else: 
        skillsToBeUpdated = [skill]
    
    if verify: 
        #TODO verifyUpdateRequest(skillsToBeUpdated) and return based on result
        print("Would have verified here")

    #TODO call updateSkills(skillsToBeUpdated)
        
    print(f"Updating {skill}")


if __name__ == "__main__":
    app()
