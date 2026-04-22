from __future__ import annotations

from datetime import datetime
from typing import Any

from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.table import Table


class JarvisConsoleUI:
    def __init__(self) -> None:
        self.console = Console()
        self.state: dict[str, Any] = {
            "mode": "local",
            "wakeword": "jarvis",
            "last_heard": "-",
            "last_user": "-",
            "last_reply": "-",
            "mcp_servers": 0,
            "status": "starting",
            "updated": datetime.utcnow().isoformat(),
        }

    def set(self, **kwargs: Any) -> None:
        self.state.update(kwargs)
        self.state["updated"] = datetime.utcnow().isoformat()

    def render(self) -> Panel:
        tbl = Table(show_header=False, box=None)
        for k in ["status", "mode", "wakeword", "mcp_servers", "last_heard", "last_user", "last_reply", "updated"]:
            tbl.add_row(f"[bold cyan]{k}[/]", str(self.state[k]))
        return Panel(tbl, title="JARVIS // LIVE OPS", border_style="bright_blue")

    def run_live(self):
        return Live(self.render(), refresh_per_second=4, console=self.console)
