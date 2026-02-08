from typing import List, Set

from rich.console import Console
from rich.live import Live
from rich.text import Text

from zxdf.view.symbols import SYMBOL_BULLET, SYMBOL_UNSELECTED
from zxdf.view.terminal import read_key


def render_picker(skills: List[dict], cursor: int, selected: Set[int]) -> Text:
    """Render the skill picker display."""
    text = Text()
    text.append("Select skills to update ", style="bold")
    text.append("(↑↓ navigate, space select, enter confirm, q quit)\n\n", style="dim")

    for i, skill in enumerate(skills):
        skill_name = skill["skill_name"]
        repo = skill["repository"]
        tools = skill["tools"]
        pointer = "> " if i == cursor else "  "
        selected_indicator = f"{SYMBOL_BULLET} " if i in selected else f"{SYMBOL_UNSELECTED} "
        bolded = "bold" if i == cursor else ""

        text.append(Text(pointer, end=" "))
        text.append(Text(selected_indicator, end=" "))
        text.append(Text(skill_name, style=bolded, end =" "))
        text.append(Text(" - ", style=f"dim {bolded}", end = " "))
        text.append(Text(repo, style=f"dim {bolded}", end = " "))
        text.append(Text("\n    ", end =""))
        text.append(Text(f"Currently installed in {len(tools)} tool{'s' if len(tools) > 1 else ''}: ", style =f"dim {bolded}", end=" "))
        text.append(Text(",".join(tools), style=f"dim {bolded}"))
        text.append("\n")

    text.append("\n")
    count = len(selected)
    if count == 0:
        text.append("No skills selected", style="dim italic")
    elif count == 1:
        text.append("1 skill selected", style="green")
    else:
        text.append(f"{count} skills selected", style="green")

    return text


def skillPicker(console: Console, skills: List[dict]) -> List[str]:
    if not skills:
        console.print("[yellow]No skills installed[/yellow]")
        return []

    cursor = 0
    selected: Set[int] = set()

    with Live(render_picker(skills, cursor, selected), console=console, auto_refresh=False, transient=True) as live:
        while True:
            key = read_key()

            if key == "\x1b[A":  # Up arrow
                cursor = (cursor - 1) % len(skills)
            elif key == "\x1b[B":  # Down arrow
                cursor = (cursor + 1) % len(skills)
            elif key == " ":  # Space - toggle selection
                if cursor in selected:
                    selected.remove(cursor)
                else:
                    selected.add(cursor)
            elif key in ("\r", "\n"):  # Enter - confirm
                if selected:
                    break
            elif key in ("q", "Q", "\x1b"):  # q or Escape - quit
                return []
            elif key == "\x03":  # Ctrl+C
                return []

            live.update(render_picker(skills, cursor, selected))
            live.refresh()

    return [skills[i]["skill_name"] for i in sorted(selected)]
