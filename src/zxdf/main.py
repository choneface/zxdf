from typing import Annotated
import typer

app = typer.Typer()


@app.command()
def add(skill: str):
    print(f"Adding {skill} to known skills")


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