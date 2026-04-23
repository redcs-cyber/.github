from __future__ import annotations

import json
import subprocess
import threading
from dataclasses import dataclass
from queue import Empty
from queue import Queue
from typing import Any


@dataclass
class MCPServerSpec:
    name: str
    command: list[str]


class StdioMCPClient:
    CLIENT_INFO = {"name": "jarvis", "version": "0.1.0"}

    def __init__(self, spec: MCPServerSpec) -> None:
        self.spec = spec
        self.proc = subprocess.Popen(
            spec.command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
        )
        self._id = 0
        self._responses: Queue[dict[str, Any]] = Queue()
        self._request_lock = threading.Lock()
        self._reader = threading.Thread(target=self._read_stdout, daemon=True)
        self._reader.start()

    def _read_stdout(self) -> None:
        assert self.proc.stdout is not None
        for line in self.proc.stdout:
            line = line.strip()
            if not line:
                continue
            try:
                self._responses.put(json.loads(line))
            except json.JSONDecodeError:
                continue

    def _request(self, method: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        with self._request_lock:
            request_id = self._id + 1
            self._id = request_id
            payload = {
                "jsonrpc": "2.0",
                "id": request_id,
                "method": method,
                "params": params or {},
            }
            assert self.proc.stdin is not None
            self.proc.stdin.write(json.dumps(payload) + "\n")
            self.proc.stdin.flush()

            while True:
                try:
                    msg = self._responses.get(timeout=30)
                except Empty as exc:
                    raise TimeoutError(f"MCP request timed out: {method}") from exc

                msg_id = msg.get("id")
                if msg_id is None:
                    continue
                if msg_id == request_id:
                    if "error" in msg:
                        raise RuntimeError(f"MCP request failed ({method}): {msg['error']}")
                    return msg

    def _notify(self, method: str, params: dict[str, Any] | None = None) -> None:
        payload = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params or {},
        }
        with self._request_lock:
            assert self.proc.stdin is not None
            self.proc.stdin.write(json.dumps(payload) + "\n")
            self.proc.stdin.flush()

    def initialize(self) -> dict[str, Any]:
        return self._request(
            "initialize",
            {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": self.CLIENT_INFO,
            },
        )

    def notify_initialized(self) -> None:
        self._notify("notifications/initialized", {})

    def list_tools(self) -> dict[str, Any]:
        return self._request("tools/list", {})

    def call_tool(self, name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        return self._request("tools/call", {"name": name, "arguments": arguments})

    def close(self) -> None:
        self.proc.terminate()
