
from rich.console import Group, RenderableType
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.spinner import Spinner

from zxdf.view.symbols import SYMBOL_FAIL, SYMBOL_OK


class Action():
    def __init__(self, console) -> None:
        self._console = console
        self._rows = []
        self._live = Live(self._render(), console=self._console, refresh_per_second=20, transient=False)
        self._live.start()

    def header(self, header: Panel):
        self._rows.append(header)
        self._rows.append(Text(""))
        self._refresh()

    def info(self, title: str):
        self._rows.append(Text(title))
        self._refresh()

    def okLine(self, title: str):
        self._rows.append(Text(f"{SYMBOL_OK} {title}"))
        self._refresh()

    def addSpinner(self, title: str, f):
        idx = len(self._rows)
        self._rows.append(Group(Text(" ", end=""), Spinner("dots", text=title)))
        self._refresh()

        try:
            result = f()
        except Exception:
            self._rows[idx] = Text(f"{SYMBOL_FAIL} {title}")
            self._refresh()
            raise
        else:
            self._rows[idx] = Text(f"{SYMBOL_OK} {title}")
            self._refresh()
            return result

    def ok(self, rows):
        self._live.update(self._success_result(rows))
        self._live.stop()

    def fatal(self, error: str, hint: str): 
        self._live.update(self._error_renderable(error, hint), refresh=True)
        self._live.stop()

    def _success_result(self, rows) -> RenderableType:
        normal_render = self._render()
        table = Table()
        table.add_column("Skill")
        table.add_column("Action")
        table.add_column("Tools")
        table.add_column("Notes")

        for row in rows:
            table.add_row(row["skill"], row["action"], row["tools"], row["notes"])

        return Group(normal_render, "\nResult", table)

    def _error_renderable(self, error: str, hint: str) -> RenderableType:
        message = f"{error} - {hint}"
        panel = Panel(message, title="ERROR")
        return panel

    def _refresh(self):
        self._live.update(self._render(), refresh=True)

    def _render(self) -> RenderableType:
        lines = []
        for row in self._rows:
            if isinstance(row, str): 
                lines.append(f"{row}\n")
            else:
                lines.append(row)
        return Group(*lines)
