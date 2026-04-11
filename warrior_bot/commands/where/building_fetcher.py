"""Building fetcher subsystem for the Where Facade."""

import json
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any

DATA_FILE = Path(__file__).parent / "data" / "locations.json"


def _search_details(details: Any, query: str) -> str | None:
    """Recursively search a details dict/str for *query*.

    Returns a human-readable location hint if found, else None.
    """
    if isinstance(details, str):
        if query in details.lower():
            return details
        return None
    if isinstance(details, dict):
        for key, value in details.items():
            if query in key.lower():
                hint = value if isinstance(value, str) else key
                return hint
            found = _search_details(value, query)
            if found:
                return found
    return None


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

        details_hits = self._search_in_details(q)
        if details_hits:
            return details_hits

        scored = []
        for b in self._buildings:
            ratio = SequenceMatcher(None, q, b["name"].lower()).ratio()
            if ratio >= 0.5:
                scored.append((ratio, b))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [b for _, b in scored]

    def _search_in_details(self, query: str) -> list[dict[str, Any]]:
        """Search inside the details/food fields of buildings."""
        results = []
        for b in self._buildings:
            details = b.get("details")
            if not details:
                continue
            hint = _search_details(details, query)
            if hint:
                entry = dict(b)
                entry["detail_hint"] = hint
                results.append(entry)
        return results
