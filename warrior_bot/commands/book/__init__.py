"""Book command -- reserve rooms on EMS via headless Playwright."""

from __future__ import annotations

import sys

import click
from colorama import Fore, Style

STEP_COLOR = Fore.GREEN
ERR_COLOR = Fore.RED
INFO_COLOR = Fore.YELLOW


def _step(msg: str) -> None:
    click.echo(f"\n{STEP_COLOR}>> {msg}{Style.RESET_ALL}")


def _info(msg: str) -> None:
    click.echo(f"{INFO_COLOR}   {msg}{Style.RESET_ALL}")


def _error(msg: str) -> None:
    click.echo(f"{ERR_COLOR}   {msg}{Style.RESET_ALL}")


@click.command()
@click.argument("building", nargs=-1)
@click.option("--headed", is_flag=True, help="Show the browser window for debugging.")
def book(building: tuple[str, ...], headed: bool):
    """Book a room on EMS (ems.wayne.edu) from the terminal.

    Optionally pass a BUILDING name to skip the template menu:

    \b
      wb book lounge space
      wb book "state hall"
      wb book STEM
    """
    try:
        from playwright.sync_api import TimeoutError as PwTimeout
    except ImportError:
        _error(
            "Playwright is not installed. Run:\n"
            "      pip install playwright && playwright install chromium"
        )
        sys.exit(1)

    from warrior_bot.commands.book import ems_pages, prompts

    def authenticate(page):
        _step("Navigating to EMS...")
        ems_pages.navigate_to_ems(page)

        if ems_pages.is_on_ems(page):
            _info("Session is still active -- skipping login.")
            return page

        if page.locator("#signin-panel").is_visible():
            _info("EMS sign-in page detected -- clicking Sign In...")
            ems_pages.handle_ems_sign_in(page)

            if ems_pages.is_on_ems(page):
                _info("SSO completed automatically -- session restored.")
                return page

        if "Error.aspx" in page.url:
            _info("Cached session is stale -- starting fresh...")
            ems_pages.clear_stale_session(page)

        _info("Redirecting to login...")
        ems_pages.navigate_to_login(page)

        if not ems_pages.is_login_page(page):
            _info("Waiting for login page...")
            try:
                page.wait_for_url("**/login.wayne.edu/**", timeout=15_000)
            except PwTimeout:
                pass

        if not ems_pages.is_login_page(page):
            _error("Could not reach the login page.")
            sys.exit(1)

        _step("WSU Login")
        access_id, password = prompts.prompt_credentials()

        _info("Submitting credentials...")
        ems_pages.fill_login_credentials(page, access_id, password)

        if "login.wayne.edu" in page.url:
            _error("Login failed -- invalid AccessID or password. " "Please try again.")
            sys.exit(1)

        ems_pages.handle_ms_trust_prompt(page)

        if "microsoftonline.com" in page.url:
            page.wait_for_timeout(2000)

        if not ems_pages.is_on_ems(page):
            mfa_options = ems_pages.get_mfa_options(page)
            if mfa_options:
                _step("Multi-Factor Authentication")
                names = [o["name"] for o in mfa_options]
                idx = prompts._numbered_menu(names, "Select verification method")
                ems_pages.click_mfa_option(page, idx)

                match_code = ems_pages.get_mfa_number_match(page)
                if not match_code:
                    _error(
                        "Could not retrieve the number match code. Please try again."
                    )
                    sys.exit(1)
                _step(f"Enter this number in your Authenticator app: {match_code}")
                _info("Waiting for verification...")
            else:
                _step("Waiting for authentication to complete...")

            try:
                ems_pages.wait_for_ems_after_login(page, timeout_ms=120_000)
            except PwTimeout:
                _error(
                    "Timed out waiting for MFA approval (2 min). " "Please try again."
                )
                sys.exit(1)

        ems_pages.handle_stay_signed_in(page)

        _info("Authentication successful!")
        return page

    def select_template(page, query: str | None = None) -> None:
        _step("Loading reservation templates...")

        templates = ems_pages.scrape_templates(page)

        if not templates:
            _error("No reservation templates found on the page.")
            _error(f"Current URL: {page.url}")
            _error(f"Page title: {page.title()}")
            sys.exit(1)

        _info(f"Found {len(templates)} template(s).")

        if query:
            matches = prompts.fuzzy_match_templates(query, templates)
            if len(matches) == 1:
                selected = matches[0]
                _info(f"Auto-selected: {selected['name']}")
            elif len(matches) > 1 and matches[0]["name"].lower() == query.lower():
                selected = matches[0]
                _info(f"Auto-selected: {selected['name']}")
            elif matches:
                _info(f"Multiple matches for '{query}':")
                selected = prompts.prompt_template(matches)
            else:
                _info(f"No match for '{query}' -- showing all templates.")
                selected = prompts.prompt_template(templates)
        else:
            selected = prompts.prompt_template(templates)

        _info(f"Selected: {selected['name']}")
        ems_pages.click_template_book_now(page, int(selected["index"]))

    def search_and_select_room(page) -> None:
        _step("Room Search")

        booking_date = prompts.prompt_date()
        start_time = prompts.prompt_start_time()
        end_time = prompts.prompt_end_time()

        _info("Filling date and time...")
        ems_pages.fill_date(page, booking_date)
        ems_pages.fill_start_time(page, start_time)
        ems_pages.fill_end_time(page, end_time)

        _info("Searching for available rooms...")
        ems_pages.click_search(page)

        rooms = ems_pages.scrape_rooms(page)
        if not rooms:
            _error(
                "No rooms found for the given criteria. " "Try different dates/times."
            )
            sys.exit(1)

        _info(f"Found {len(rooms)} room(s).")
        selected_room = prompts.prompt_room(rooms)

        _info(f"Selected: {selected_room['name']}")
        ems_pages.click_room_add(page, selected_room["row_index"])

        attendees = prompts.prompt_attendees()
        ems_pages.fill_attendees(page, attendees)

        _info("Adding room to cart...")
        ems_pages.click_add_room_modal(page)

        _info("Proceeding to Reservation Details...")
        ems_pages.click_next_step(page)

    def fill_and_submit_reservation(page) -> None:
        _step("Reservation Details")

        event_name = prompts.prompt_event_name()
        ems_pages.fill_event_name(page, event_name)

        try:
            event_types = ems_pages.get_event_type_options(page)
            if event_types:
                event_type = prompts.prompt_event_type(event_types)
                ems_pages.select_event_type(page, event_type)
        except Exception:
            pass

        phone = prompts.prompt_contact_phone()
        ems_pages.fill_contact_phone(page, phone)

        email = prompts.prompt_contact_email()
        ems_pages.fill_contact_email(page, email)

        try:
            av_sel = page.locator("select[aria-label*='audio/visual'], select#26").first
            if av_sel.is_visible(timeout=2000):
                av_choice = prompts.prompt_av_technology()
                ems_pages.fill_av_technology(page, av_choice)
        except Exception:
            pass

        try:
            desc_el = page.locator(
                "textarea[aria-label*='description'], textarea#13"
            ).first
            if desc_el.is_visible(timeout=2000):
                description = prompts.prompt_event_description()
                ems_pages.fill_event_description(page, description)
        except Exception:
            pass

        try:
            time_el = page.locator(
                "input[aria-label*='actual event time'], input#udf7"
            ).first
            if time_el.is_visible(timeout=2000):
                event_time = prompts.prompt_event_time()
                ems_pages.fill_actual_event_time(page, event_time)
        except Exception:
            pass

        if not prompts.prompt_confirm("Submit this reservation?"):
            _info("Reservation cancelled.")
            return

        _info("Submitting reservation...")
        ems_pages.click_create_reservation(page)

        _step("Reservation created successfully!")

    _step("Starting EMS Room Booking")

    building_query = " ".join(building).strip() or None

    with ems_pages.EMSBrowser(headed=headed) as browser:
        try:
            page = authenticate(browser.page)
            select_template(page, query=building_query)
            search_and_select_room(page)
            fill_and_submit_reservation(page)
        except PwTimeout as exc:
            _error(f"Operation timed out: {exc}")
            sys.exit(1)
        except Exception as exc:
            _error(f"Unexpected error: {exc}")
            sys.exit(1)
