from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class JsonStore:
    def __init__(self, file_path: Path) -> None:
        self.file_path = file_path
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.file_path.exists():
            self.file_path.write_text("[]", encoding="utf-8")

    def read_all(self) -> list[dict[str, Any]]:
        try:
            data = json.loads(self.file_path.read_text(encoding="utf-8"))
            if isinstance(data, list):
                return data
            return []
        except json.JSONDecodeError:
            return []

    def append(self, item: dict[str, Any]) -> None:
        data = self.read_all()
        data.append(item)
        self.file_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
