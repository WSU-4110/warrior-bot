"""Facade for the Where command."""

from warrior_bot.commands.where.building_fetcher import BuildingFetcher
from warrior_bot.commands.where.restaurant_fetcher import RestaurantFetcher
from warrior_bot.commands.where.staff_fetcher import StaffFetcher, StaffFetchError
from warrior_bot.commands.where.staff_formatter import StaffFormatter


class WhereFacade:

    def __init__(self) -> None:
        self._staff_fetcher = StaffFetcher()
        self._staff_formatter = StaffFormatter()
        self._restaurant_fetcher = RestaurantFetcher()
        self._building_fetcher = BuildingFetcher()

    def search_staff(self, name: str) -> tuple[str, bool]:
        try:
            staff, soup = self._staff_fetcher.fetch(name)
        except StaffFetchError as e:
            return f"\033[31m[ERROR] {e}\033[0m", False

        if not staff:
            return self._staff_formatter.format_not_found(), False

        full_name = name.title()
        count = len(staff)

        if count == 1:
            if soup is None:
                return self._staff_formatter.format_not_found(), False
            return self._staff_formatter.format_single(full_name, soup), True
        else:
            return self._staff_formatter.format_multiple(staff, count), True

    def search_restaurants(self, category: str = "all") -> tuple[str, bool]:
        if category == "campus":
            restaurants = self._restaurant_fetcher.get_on_campus()
            header = "On-Campus Dining Locations"
        elif category == "awd":
            restaurants = self._restaurant_fetcher.get_anthony_wayne_drive()
            header = "Anthony Wayne Drive Restaurants"
        else:
            restaurants = self._restaurant_fetcher.get_all()
            header = "All Campus & Nearby Restaurants"

        if not restaurants:
            return "\033[31m[ERROR] No restaurant data found.\033[0m", False

        return self._format_restaurant_list(header, restaurants), True

    def search_restaurants_by_name(self, query: str) -> tuple[str, bool]:
        results = self._restaurant_fetcher.search(query)

        if not results:
            return (
                f"\033[31m[ERROR] No restaurant matching '{query}' found.\033[0m\n"
                " Try 'wb where --restaurants' to see all available locations.",
                False,
            )

        header = f"Search results for '{query}'"
        return self._format_restaurant_list(header, results), True

    def search_building(self, query: str) -> tuple[str, bool]:
        results = self._building_fetcher.search(query)

        if not results:
            return (
                f"\033[31m[ERROR] No building matching '{query}' found.\033[0m\n"
                " Try 'wb where -b' with a different name or building code.",
                False,
            )

        return self._format_building_list(results), True

    def _format_building_list(self, buildings: list[dict]) -> str:
        BOLD = "\033[1m"
        RESET = "\033[0m"
        DIM = "\033[2m"

        lines = [f"\n{BOLD}Building Search Results{RESET} ({len(buildings)} found)\n"]
        lines.append("-" * 40)

        for b in buildings:
            lines.append(f"{BOLD}{b['name']}{RESET} ({b.get('code', '')})")
            lines.append(f"  Address : {b['address']}")
            lines.append(f"  Type    : {b.get('type', '')}")
            if b.get("description"):
                lines.append(f"  {DIM}{b['description']}{RESET}")
            lines.append("")

        return "\n".join(lines)

    def _format_restaurant_list(self, header: str, restaurants: list[dict]) -> str:
        BOLD = "\033[1m"
        RESET = "\033[0m"
        DIM = "\033[2m"

        lines = [f"\n{BOLD}{header}{RESET} ({len(restaurants)} locations)\n"]
        lines.append("-" * 40)

        for r in restaurants:
            lines.append(f"{BOLD}{r['name']}{RESET}")
            lines.append(f"  Address : {r['address']}")
            if r.get("phone"):
                lines.append(f"  Phone   : {r['phone']}")
            lines.append(f"  Type    : {r['type']}")
            if r.get("notes"):
                lines.append(f"  {DIM}{r['notes']}{RESET}")
            lines.append("")

        return "\n".join(lines)
