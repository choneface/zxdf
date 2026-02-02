from typing import Annotated
from rich.console import Console
import typer

from zxdf.skill_manager import addSkill

app = typer.Typer()
console = Console()

@app.command()
def add(skill: str):
    with console.status("[bold green]Adding skill...") as status:
        addSkill(skill)
    console.print("[bold green]Skill added")


@app.command()
def update(skill: Annotated[str, typer.Argument()] = ""):
    if skill == "":
        ans = input("Are you sure you want to update all skills? (Y/n): ")
        if ans == "Y":
            print("Updating all skills...") 
            return
        else:
            print("No worries, exiting")
            return 
        
    print(f"Updating {skill}")


if __name__ == "__main__":
    app()
