from typing import List

from rich.console import Console
from rich.live import Live
from rich.text import Text

from readchar import readkey, key


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
            try:
                key_press = readkey()
                if key_press in ("Y", "y"):
                    return True
                if key_press in ("N", "n", "q", key.ESC):
                    return False
            except KeyboardInterrupt:
                # Handle Ctrl+C
                return False
