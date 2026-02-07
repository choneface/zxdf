from typing import Annotated

import typer
from rich.console import Console

from zxdf.services import addSkill, updateSkills

skill_app = typer.Typer(help="Manage AI skills")
console = Console()


@skill_app.command()
def add(skill: Annotated[str, typer.Argument(help="[bold]format: author/skillname")]):
    """Add a skill by providing skill slug."""
    addSkill(console, skill)


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
    updateSkills(console, skill, verify, update_all)
