from typing import List, Set

from rich.console import Console
from rich.live import Live
from rich.text import Text

from readchar import readkey, key


def render_picker(skills: List[str], cursor: int, selected: Set[int]) -> Text:
    """Render the skill picker display."""
    text = Text()
    text.append("Select skills to update ", style="bold")
    text.append("(↑↓ navigate, space select, enter confirm, q quit)\n\n", style="dim")

    for i, skill in enumerate(skills):
        # Checkbox
        if i in selected:
            checkbox = "[×] "
            checkbox_style = "green bold"
        else:
            checkbox = "[ ] "
            checkbox_style = "dim"

        # Cursor indicator and highlighting
        if i == cursor:
            text.append("> ", style="cyan bold")
            text.append(checkbox, style=checkbox_style)
            text.append(skill, style="cyan bold")
        else:
            text.append("  ", style="")
            text.append(checkbox, style=checkbox_style)
            text.append(skill, style="")

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


def skillPicker(console: Console, skills: List[str]) -> List[str]:
    if not skills:
        console.print("[yellow]No skills installed[/yellow]")
        return []

    cursor = 0
    selected: Set[int] = set()

    with Live(render_picker(skills, cursor, selected), console=console, auto_refresh=False, transient=True) as live:
        while True:
            try:
                key_press = readkey()

                if key_press == key.UP:
                    cursor = (cursor - 1) % len(skills)
                elif key_press == key.DOWN:  # Down arrow
                    cursor = (cursor + 1) % len(skills)
                elif key_press == key.SPACE:  # Space - toggle selection
                    if cursor in selected:
                        selected.remove(cursor)
                    else:
                        selected.add(cursor)
                elif key_press == key.ENTER:
                    if selected:
                        break
                elif key_press in ("q", "Q", "\x1b"):  # q or Escape - quit
                    return []
            except KeyboardInterrupt:
                # Handle Ctrl+C
                return []

            live.update(render_picker(skills, cursor, selected))
            live.refresh()

    return [skills[i] for i in sorted(selected)]
