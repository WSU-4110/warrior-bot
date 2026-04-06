"""Restaurant fetcher subsystem for the Where Facade."""

import json
from pathlib import Path

DATA_FILE = Path(__file__).parent.parent.parent / "data" / "restaurants.json"


class RestaurantFetcher:

    def __init__(self) -> None:
        self._data: dict = {}

    def _load(self) -> None:
        if not self._data:
            with open(DATA_FILE, "r") as f:
                self._data = json.load(f)

    def get_all(self) -> list[dict]:
        self._load()
        seen = set()
        combined = []
        for restaurant in self._data.get("on_campus", []) + self._data.get(
            "anthony_wayne_drive", []
        ):
            if restaurant["name"] not in seen:
                seen.add(restaurant["name"])
                combined.append(restaurant)
        return combined

    def get_on_campus(self) -> list[dict]:
        self._load()
        return self._data.get("on_campus", [])

    def get_anthony_wayne_drive(self) -> list[dict]:
        self._load()
        return self._data.get("anthony_wayne_drive", [])

    def search(self, query: str) -> list[dict]:
        self._load()
        query_lower = query.lower()
        return [r for r in self.get_all() if query_lower in r["name"].lower()]
