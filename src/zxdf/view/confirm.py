from typing import List

from rich.console import Console
from rich.live import Live
from rich.text import Text

from zxdf.view.terminal import read_key


def confirm(console: Console, message: str, items: List[str]) -> bool:
    prompt = Text()
    prompt.append(f"{message}\n\n", style="bold yellow")
    for item in items:
        prompt.append(f"  - {item}\n")
    prompt.append("\nPress ", style="dim")
    prompt.append("Y", style="bold green")
    prompt.append(" to confirm or ", style="dim")
    prompt.append("n", style="bold red")
    prompt.append(" to cancel", style="dim")

    with Live(prompt, console=console, auto_refresh=False, transient=True):
        while True:
            key = read_key()
            if key in ("Y", "y"):
                return True
            if key in ("N", "n", "q", "\x1b", "\x03"):
                return False
