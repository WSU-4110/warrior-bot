"""Staff formatter subsystem for the Where Facade."""
import requests
from bs4 import BeautifulSoup


class StaffFormatter:

    RED = "\033[31m"
    BOLD = "\033[1m"
    RESET = "\033[0m"

    def format_single(self, full_name: str, soup: BeautifulSoup) -> str:
        info = f"{full_name} "
        errors = ""
        row = soup.select_one("table.table-stack tbody tr")
        if row is None:
            return self.format_not_found()

        cols = row.find_all("td")
        if len(cols) < 5:
            return self.format_not_found()

        title = cols[1].get_text(strip=True)
        dept = cols[2].get_text(strip=True)
        phone = cols[3].get_text(strip=True)
        email = cols[4].get_text(strip=True)
        if title:
            info += f"- {title}\n"
        if dept:
            info += (
                f"Department: {self.BOLD}{dept}{self.RESET} department.\n"
            )
        else:
            errors += (
                self.RED
                + "[ERROR] This staff member does not have a department.\n"
                + self.RESET
            )
        if email:
            info += f"Email: {self.BOLD}{email}{self.RESET}.\n"
        else:
            errors += (
                self.RED
                + "[ERROR] This staff member does not have a registered email.\n"
                + self.RESET
            )
        if phone:
            info += f"Phone Number: {self.BOLD}{phone}{self.RESET}.\n"
        else:
            errors += (
                self.RED
                + "[ERROR] This staff member does not have a registered phone number.\n"
                + self.RESET
            )
        name_col = cols[0]
        link_tag = name_col.find("a")
        href = link_tag.get("href") if link_tag else None
        if isinstance(href, str) and href:
            link = "https://wayne.edu" + href

            staff_office_loc = format_office_search(self.BOLD, self.RESET, link)
            if not staff_office_loc:
                errors += (
                    f"{self.RED}[ERROR] No information found on offices.{self.RESET}\n"
                    f" - For possible office locations, look at their department or instructors syllabus\n"
                )
                if email:
                    errors += (
                        f" - For more information of office locations, "
                        f"you can email them at {self.BOLD}{email}{self.RESET}\n"
                    )
            else:
                info += (
                    f"You may find their {self.BOLD}office{self.RESET} at: \n{staff_office_loc}\n"
                )
            info += (
                f"For more information on {full_name},"
                f" visit their web page: {link}\n"
            )
        else:
            errors += (
                self.RED
                + "[ERROR] This staff member does not have a web page link.\n"
                + "Office information cannon be found without a registered web page"
                + self.RESET
            )
        return info + errors

    def format_multiple(self, staff: list[str], count: int) -> str:
        lines = [
            f"{count} instructors found. Please insert the full name using wb where"
        ]
        for name in staff:
            lines.append(f" - {name}")
        return "\n".join(lines)

    def format_not_found(self) -> str:
        return (
            f"{self.RED}[ERROR] No information on this staff member"
            f" found!{self.RESET}\n"
            " Possible Issues:\n"
            " - Incorrect Spelling\n"
            " - Instructor may be new\n"
            " - Instructor may be a Teacher Assistant\n"
            " For building use -building or -b after the name\n"
            " Please try again using wb where"
        )

def format_office_search(BOLD, RESET, link):
    #html search
    staff_office_str = ""

    try:
        response = requests.get(link)
        response.raise_for_status()
    except requests.RequestException:
        return staff_office_str

    soup = BeautifulSoup(response.text, "html.parser")

    building = ""
    office = ""
    room = ""
    address = ""

    for section in soup.findAll("div"):

        text = section.get_text(separator=" ", strip=True)

        lower_text = text.lower()

        #keywords to find office
        if lower_text.startswith("office:"):
            office = text.split(":", 1)[1].strip()
        elif lower_text.startswith("building:"):
            building = text.split(":", 1)[1].strip()
        elif lower_text.startswith("room:"):
            room = text.split(":", 1)[1].strip()
        elif lower_text.startswith("address:"):
            address = text.split(":", 1)[1].strip()


    if office:
        staff_office_str += (
            f"{BOLD}Office:{RESET} {office}\n"
        )
    if room:
        staff_office_str += (
            f"{BOLD}Room:{RESET} {room}\n"
        )
    if building:
        staff_office_str += (
            f"{BOLD}Building:{RESET} {building}\n"
        )
    if address:
        staff_office_str += (
            f"{BOLD}Address:{RESET} {address}\n"
        )

    return staff_office_str


