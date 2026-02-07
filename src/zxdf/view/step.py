
from rich.console import Group, RenderableType
from rich.live import Live
from rich.panel import Panel
from rich.table import Table


class Step():
    def __init__(self, console, title) -> None:
        self._title = title
        self._console = console
        self._rows = []
        self._live = Live(self._render(), console=self._console, refresh_per_second=20, transient=False)
        self._live.start()

    def updateTitle(self, title: str):
        self._title = title
        self._live.update(self._render(), refresh=True)

    def updateSpinner(self, title: str):
        self._rows[-1] = title
        self._live.update(self._render(), refresh=True)

    def addSpinner(self, title: str):
        self._rows.append(title)
        self._live.update(self._render(), refresh=True)

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

        return Group(normal_render, "Result", table)

    def _error_renderable(self, error: str, hint: str) -> RenderableType:
        message = f"{error} - {hint}"
        panel = Panel(message, title="ERROR")
        return panel

    def _refresh(self):
        self._live.update(self._render(), refresh=True)

    def _render(self) -> RenderableType:
        lines = []
        for row in self._rows:
            lines.append(f"{row}\n")
        return Group(self._title, *lines)
