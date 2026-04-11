"""Building fetcher subsystem for the Where Facade."""

import json
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any

DATA_FILE = Path(__file__).parent / "data" / "locations.json"


class BuildingFetcher:

    def __init__(self) -> None:
        self._buildings: list[dict[str, Any]] = []

    def _load(self) -> None:
        if self._buildings:
            return
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
        for buildings in data.get("categories", {}).values():
            self._buildings.extend(buildings)

    def get_all(self) -> list[dict[str, Any]]:
        self._load()
        return list(self._buildings)

    def search(self, query: str) -> list[dict[str, Any]]:
        self._load()
        q = query.lower()

        exact = [
            b
            for b in self._buildings
            if q == b["name"].lower() or q == b.get("code", "").lower()
        ]
        if exact:
            return exact

        substring = [b for b in self._buildings if q in b["name"].lower()]
        if substring:
            return substring

        scored = []
        for b in self._buildings:
            ratio = SequenceMatcher(None, q, b["name"].lower()).ratio()
            if ratio >= 0.5:
                scored.append((ratio, b))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [b for _, b in scored]
