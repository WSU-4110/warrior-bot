"""Staff fetcher subsystem for the Where Facade."""

import requests
from bs4 import BeautifulSoup


class StaffFetcher:

    BASE_URL = "https://wayne.edu/people"

    def fetch(self, name: str) -> tuple[list[str], "BeautifulSoup | None"]:
        query = "+".join(name.split()).title()
        url = f"{self.BASE_URL}?type=people&q={query}"

        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.RequestException as e:
            raise StaffFetchError(
                "Could not gain access to URL. "
                "Please make sure you have a stable internet connection."
            ) from e

        soup = BeautifulSoup(response.text, "html.parser")
        staff = []
        for row in soup.select("table.table-stack tbody tr"):
            first_cell = row.find("td")
            if first_cell is not None:
                staff.append(first_cell.get_text(strip=True))

        return staff, soup


class StaffFetchError(Exception):
    pass
