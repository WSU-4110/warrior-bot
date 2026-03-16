"""Playwright page interaction helpers for EMS (ems.wayne.edu)."""

from __future__ import annotations

import time
from pathlib import Path
from typing import Any

from playwright.sync_api import Page
from playwright.sync_api import TimeoutError as PwTimeout

EMS_BASE = "https://ems.wayne.edu"
EMS_HOME = f"{EMS_BASE}/EmsWebApp/"
EMS_LOGIN = f"{EMS_BASE}/EmsWebApp/SamlAuth.aspx"
EMS_ROOM_REQUEST = f"{EMS_BASE}/EmsWebApp/RoomRequest.aspx"
DATA_DIR = Path.home() / ".warrior-bot"
BROWSER_DATA_DIR = DATA_DIR / "browser-data"


def navigate_to_ems(page: Page) -> None:
    page.goto(EMS_HOME, wait_until="networkidle")


def navigate_to_login(page: Page) -> None:
    page.goto(EMS_LOGIN, wait_until="networkidle")


def is_login_page(page: Page) -> bool:
    """Check if we're on any login page (WSU or Microsoft)."""
    url = page.url
    return (
        "login.wayne.edu" in url
        or "login.microsoftonline.com" in url
        or "login.live.com" in url
    )


def fill_login_credentials(page: Page, access_id: str, password: str) -> None:
    """Fill credentials on whichever login page we're on (WSU or Microsoft)."""
    url = page.url

    if "login.wayne.edu" in url:
        page.locator("#accessid").fill(access_id)
        page.locator("#passwd").fill(password)
        page.locator("#login-button").click()

        try:
            page.wait_for_url(lambda u: "login.wayne.edu" not in u, timeout=10_000)
        except PwTimeout:
            pass

        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(2000)
    elif "login.microsoftonline.com" in url or "login.live.com" in url:
        page.locator('input[type="email"]').fill(access_id)
        page.locator('input[type="submit"]').click()
        page.wait_for_load_state("networkidle")
        page.locator('input[type="password"]').fill(password)
        page.locator('input[type="submit"]').click()
        page.wait_for_load_state("networkidle")


def handle_ms_trust_prompt(page: Page) -> None:
    """Click 'Continue' on the 'Do you trust wayne.edu?' Microsoft prompt."""
    try:
        continue_btn = page.locator("#idSIButton9, button:has-text('Continue')")
        if continue_btn.first.is_visible(timeout=5000):
            continue_btn.first.click()
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(2000)
    except PwTimeout:
        pass


def get_mfa_options(page: Page) -> list[dict[str, str]]:
    """
    Scrape MFA verification options from the Microsoft
    'Verify your identity' page.
    """
    options: list[dict[str, str]] = []
    tiles = page.locator("div.row.tile")
    count = tiles.count()
    for i in range(count):
        tile = tiles.nth(i)
        text = tile.inner_text().strip()
        if text:
            options.append({"name": text, "index": str(i)})
    return options


def click_mfa_option(page: Page, index: int) -> None:
    """Click the selected MFA verification option."""
    tiles = page.locator("div.row.tile")
    tiles.nth(index).click()
    page.wait_for_timeout(2000)


def get_mfa_number_match(page: Page, timeout_ms: int = 30_000) -> str | None:
    """Scrape the number-match code shown on the MFA approval page (e.g. '84').

    Polls for the number-match element to appear after the MFA option tile is
    clicked and the page transitions to the approval screen.
    """
    deadline = time.time() + timeout_ms / 1000
    while time.time() < deadline:
        try:
            el = page.locator("#idRichContext_DisplaySign")
            if el.is_visible(timeout=2_000):
                text = el.inner_text().strip()
                if text:
                    return text
        except PwTimeout:
            pass
        page.wait_for_timeout(1_000)
    return None


def handle_stay_signed_in(page: Page) -> None:
    """Click 'Yes' on the 'Stay signed in?' prompt if visible."""
    try:
        yes_btn = page.locator("#idSIButton9")
        if yes_btn.is_visible(timeout=500):
            yes_btn.click()
            try:
                page.wait_for_url(
                    lambda u: "microsoftonline.com" not in u
                    and "login.wayne.edu" not in u,
                    timeout=30_000,
                )
            except PwTimeout:
                pass
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(3000)
    except PwTimeout:
        pass


def wait_for_ems_after_login(page: Page, timeout_ms: int = 120_000) -> None:
    """Wait until we land on a valid EMS page (handles MFA delay).

    Polls the current URL in a loop so we can handle intermediate pages
    like "Stay signed in?" that appear between MFA approval and the EMS
    redirect.
    """
    deadline = time.time() + timeout_ms / 1000
    error_count = 0

    while time.time() < deadline:
        cur_url = page.url

        if EMS_BASE.lower() in cur_url.lower():
            if "Error.aspx" in cur_url:
                error_count += 1
                if error_count <= 3:
                    page.goto(EMS_HOME, wait_until="networkidle")
                    handle_stay_signed_in(page)
                    page.wait_for_timeout(2000)
                else:
                    return
                continue
            return

        handle_stay_signed_in(page)
        page.wait_for_timeout(1000)

    raise PwTimeout(f"Timed out after {timeout_ms}ms waiting for EMS")


def is_on_ems(page: Page) -> bool:
    """Check if we're on a valid EMS page (not error, not login/sign-in)."""
    if EMS_BASE not in page.url:
        return False
    if "Error.aspx" in page.url:
        return False
    if page.locator("#signin-panel").is_visible():
        return False
    return True


def handle_ems_sign_in(page: Page) -> None:
    """Click the EMS 'Sign In' button if the sign-in panel is showing.

    The EMS home page sometimes shows a sign-in panel even when we have
    valid SSO cookies.  Clicking the button triggers the SSO redirect which
    completes automatically if the session is still valid.
    """
    try:
        sign_in_btn = page.get_by_role("button", name="Sign In")
        if sign_in_btn.is_visible(timeout=2_000):
            sign_in_btn.click()
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(3000)
    except PwTimeout:
        pass


def clear_stale_session(page: Page) -> None:
    """Clear cookies so we re-authenticate with a fresh session."""
    page.context.clear_cookies()


def _ensure_ems_home(page: Page) -> None:
    """Make sure we're on a valid EMS home page, handling errors and sign-in."""
    for attempt in range(3):
        if is_on_ems(page) and "Error.aspx" not in page.url:
            if page.locator("#signin-panel").is_visible():
                handle_ems_sign_in(page)
                page.wait_for_timeout(3000)
                continue
            return

        page.goto(EMS_HOME, wait_until="networkidle")
        page.wait_for_timeout(2000)

        if page.locator("#signin-panel").is_visible():
            handle_ems_sign_in(page)
            page.wait_for_timeout(3000)


def navigate_to_room_request(page: Page) -> None:
    """Navigate to the reservation templates page via the UI.

    Direct page.goto() to RoomRequest.aspx causes Error.aspx -- the EMS
    server requires navigation through the application.
    """
    if "RoomRequest" in page.url:
        return

    _ensure_ems_home(page)

    strategies = [
        lambda: page.get_by_role("link", name="Create A Reservation").first,
        lambda: page.locator("a[href*='RoomRequest']").first,
        lambda: page.get_by_text("Create A Reservation").first,
    ]

    for strategy in strategies:
        try:
            link = strategy()
            if link.is_visible(timeout=5_000):
                link.click()
                page.wait_for_load_state("networkidle")
                page.wait_for_timeout(2000)
                if "RoomRequest" in page.url:
                    return
        except (PwTimeout, Exception):
            continue

    raise PwTimeout(
        "Could not navigate to 'Create A Reservation'. " f"Current URL: {page.url}"
    )


def scrape_templates(page: Page) -> list[dict[str, str]]:
    """Extract reservation templates (buildings) from the RoomRequest page."""
    navigate_to_room_request(page)

    try:
        page.wait_for_selector("#templates-grid .btn-primary", timeout=15_000)
    except PwTimeout:
        page.wait_for_timeout(3000)

    templates: list[dict[str, str]] = []

    rows = page.locator("#templates-grid .row:has(.btn-primary)")
    count = rows.count()

    if count == 0:
        rows = page.locator("#templates-grid .row")
        count = rows.count()

    for i in range(count):
        row = rows.nth(i)
        name = row.locator(".ellipsis-text").inner_text(timeout=2_000).strip()
        if not name:
            name = row.inner_text().split("\n")[0].strip()
        if name:
            templates.append({"name": name, "index": str(i)})

    return templates


def click_template_book_now(page: Page, index: int) -> None:
    rows = page.locator("#templates-grid .row:has(.btn-primary)")
    row = rows.nth(index)
    row.locator(".btn-primary").first.click()
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(2000)


def fill_date(page: Page, booking_date: str) -> None:
    date_input = page.locator("#booking-date-input")
    date_input.click()
    date_input.fill("")
    date_input.fill(booking_date)
    date_input.press("Tab")
    page.wait_for_timeout(500)


def fill_start_time(page: Page, start_time: str) -> None:
    start_input = page.locator("#start-time-input")
    start_input.click()
    start_input.fill("")
    start_input.fill(start_time)
    start_input.press("Tab")
    page.wait_for_timeout(500)


def fill_end_time(page: Page, end_time: str) -> None:
    end_input = page.locator("#end-time-input")
    end_input.click()
    end_input.fill("")
    end_input.fill(end_time)
    end_input.press("Tab")
    page.wait_for_timeout(500)


def click_search(page: Page) -> None:
    page.locator("button.find-a-room").first.click()
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(3000)


def scrape_rooms(page: Page) -> list[dict[str, Any]]:
    """Scrape rooms from the results table (#available-list)."""
    rooms: list[dict[str, Any]] = []

    page.wait_for_selector(
        "table#available-list tbody tr, .dynamic-filter-item-add",
        timeout=10_000,
    )

    rows = page.locator("table#available-list tbody tr")
    count = rows.count()

    for i in range(count):
        row = rows.nth(i)
        cells = row.locator("td")
        if cells.count() < 2:
            continue
        room_name = cells.nth(1).inner_text().strip() if cells.count() > 1 else ""
        if not room_name:
            continue
        location = cells.nth(2).inner_text().strip() if cells.count() > 2 else ""
        floor = cells.nth(3).inner_text().strip() if cells.count() > 3 else ""
        capacity = cells.nth(5).inner_text().strip() if cells.count() > 5 else ""

        display = room_name
        if location:
            display += f" | {location}"
        if floor:
            display += f" | {floor}"
        if capacity:
            display += f" | Cap: {capacity}"

        rooms.append({"name": display, "row_index": i})

    return rooms


def click_room_add(page: Page, row_index: int) -> None:
    """Click the green '+' add-to-cart icon on the given room row."""
    rows = page.locator("table#available-list tbody tr")
    row = rows.nth(row_index)
    add_btn = row.locator("a.add-to-cart, i.fa-plus-circle")
    add_btn.first.click()
    page.wait_for_timeout(2000)


def fill_attendees(page: Page, count: str) -> None:
    attendee_input = page.locator("#setup-add-count")
    attendee_input.wait_for(timeout=5000)
    attendee_input.fill("")
    attendee_input.fill(count)


def get_setup_type_options(page: Page) -> list[str]:
    select_el = page.locator("#setup-add-type")
    options = select_el.locator("option").all_text_contents()
    return [o.strip() for o in options if o.strip()]


def select_setup_type(page: Page, setup_type: str) -> None:
    page.locator("#setup-add-type").select_option(label=setup_type)


def click_add_room_modal(page: Page) -> None:
    """Click 'Add Room' button inside the Attendance & Setup Type modal."""
    page.locator(
        "button:has-text('Add Room'), " "input[value='Add Room']"
    ).first.click()
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(2000)


def click_next_step(page: Page) -> None:
    btn = page.locator("button#next-step-btn")
    btn.first.wait_for(state="visible", timeout=10_000)
    btn.first.click()
    page.locator("#event-name").wait_for(state="visible", timeout=30_000)


def get_event_type_options(page: Page) -> list[str]:
    select_el = page.locator("#event-type")
    options = select_el.locator("option").all_text_contents()
    return [o.strip() for o in options if o.strip()]


def fill_event_name(page: Page, name: str) -> None:
    page.locator("#event-name").fill(name)


def select_event_type(page: Page, event_type: str) -> None:
    page.locator("#event-type").select_option(label=event_type)
    page.wait_for_timeout(1000)


def fill_contact_phone(page: Page, phone: str) -> None:
    page.locator("#event-type").focus()
    for _ in range(5):
        page.keyboard.press("Tab")
    page.keyboard.type(phone)


def fill_contact_email(page: Page, email: str) -> None:
    for _ in range(2):
        page.keyboard.press("Tab")
    page.keyboard.type(email)


def fill_av_technology(page: Page, choice: str) -> None:
    """Fill the 'Will you be using audio/visual technology?' dropdown if present."""
    try:
        sel = page.locator("select[aria-label*='audio/visual'], select#26").first
        if sel.is_visible(timeout=2000):
            sel.select_option(label=choice)
    except (PwTimeout, Exception):
        pass


def fill_event_description(page: Page, description: str) -> None:
    """Fill the event description textarea if present."""
    try:
        textarea = page.locator(
            "textarea[aria-label*='description'], textarea#13"
        ).first
        if textarea.is_visible(timeout=2000):
            textarea.fill(description)
    except (PwTimeout, Exception):
        pass


def fill_actual_event_time(page: Page, event_time: str) -> None:
    """Fill the 'actual event time' input if present."""
    try:
        inp = page.locator("input[aria-label*='actual event time'], input#udf7").first
        if inp.is_visible(timeout=2000):
            inp.fill(event_time)
    except (PwTimeout, Exception):
        pass


def click_create_reservation(page: Page) -> None:
    page.locator("button.btn-success:has-text('Create Reservation')").first.click()
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(3000)


def get_browser_data_dir() -> str:
    """Return the persistent browser profile path, creating it if needed."""
    BROWSER_DATA_DIR.mkdir(parents=True, exist_ok=True)
    return str(BROWSER_DATA_DIR)


class EMSBrowser:
    """Manages a Playwright browser session using the Lazy Initialization pattern.

    The Playwright engine, browser context, and page are heavyweight resources
    (spawning a Chromium process, reading a persistent profile from disk).
    Rather than creating them eagerly, each is deferred until first access via
    properties that check for ``None`` and initialize on demand.
    """

    def __init__(self, headed: bool = False) -> None:
        self._headed = headed
        self._playwright: Any | None = None
        self._context: Any | None = None
        self._page: Page | None = None

    @property
    def playwright(self) -> Any:
        """Lazily start the Playwright engine on first access."""
        if self._playwright is None:
            from playwright.sync_api import sync_playwright

            self._playwright = sync_playwright().start()
        return self._playwright

    @property
    def context(self) -> Any:
        """Lazily launch the persistent browser context on first access."""
        if self._context is None:
            launch_args = ["--disable-blink-features=AutomationControlled"]
            if not self._headed:
                launch_args.append("--window-position=-32000,-32000")

            self._context = self.playwright.chromium.launch_persistent_context(
                get_browser_data_dir(),
                headless=False,
                viewport={"width": 1920, "height": 1080},
                user_agent=(
                    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
                ),
                args=launch_args,
            )
            self._context.set_default_timeout(120_000)
            self._context.set_default_navigation_timeout(120_000)
        return self._context

    @property
    def page(self) -> Page:
        """Lazily create a new browser page on first access."""
        if self._page is None:
            self._page = self.context.new_page()
        return self._page

    def close(self) -> None:
        """Release all resources that were initialized."""
        if self._context is not None:
            self._context.close()
        if self._playwright is not None:
            self._playwright.stop()
        self._page = None
        self._context = None
        self._playwright = None

    def __enter__(self) -> "EMSBrowser":
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()
