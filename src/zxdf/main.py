import typer

from zxdf.commands import skill_app, tool_app

app = typer.Typer(
    help="CLI tool for managing AI skills. Use skill slugs in the format: author/skillname"
)

app.add_typer(skill_app, name="skill")
app.add_typer(tool_app, name="tool")


if __name__ == "__main__":
    app()
