from typing import Annotated
from rich.console import Console
from rich.live import Live
from rich.text import Text
import typer

from zxdf.skill_manager import addSkill, getAllSkills, updateSkills
from zxdf.skill_picker import skillPicker, read_key

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
        prompt = Text()
        prompt.append("Are you sure you want to update the following skills?\n\n", style="bold yellow")
        for s in skillsToBeUpdated:
            prompt.append(f"  - {s}\n")
        prompt.append("\nPress ", style="dim")
        prompt.append("Y", style="bold green")
        prompt.append(" to confirm or ", style="dim")
        prompt.append("n", style="bold red")
        prompt.append(" to cancel", style="dim")

        with Live(prompt, console=console, auto_refresh=False, transient=True):
            while True:
                key = read_key()
                if key in ("Y", "y"):
                    break
                if key in ("N", "n", "q", "\x1b", "\x03"):
                    console.print("Exiting, no changes made")
                    return
        
    updateSkills(console, skillsToBeUpdated)


if __name__ == "__main__":
    app()
