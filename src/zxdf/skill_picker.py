import sys
import tty
import termios
from typing import List, Set
from rich.console import Console
from rich.live import Live
from rich.text import Text
from zxdf.skill_manager import getAllSkills


def read_key() -> str:
    """Read a single keypress from stdin without requiring sudo."""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
        # Handle escape sequences (arrow keys)
        if ch == "\x1b":
            ch2 = sys.stdin.read(1)
            if ch2 == "[":
                ch3 = sys.stdin.read(1)
                return f"\x1b[{ch3}"
        return ch
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


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


def skillPicker(console: Console) -> List[str]:
    """Interactive skill picker using Rich and raw terminal input."""
    skills = getAllSkills()

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

    return [skills[i] for i in sorted(selected)]
