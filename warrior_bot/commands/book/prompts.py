"""Terminal prompt helpers for the book command using click (sync, no asyncio)."""

from __future__ import annotations

import re
from datetime import date, datetime, timedelta
from difflib import SequenceMatcher
from getpass import getpass
from typing import Any

import click
from colorama import Fore, Style


def _fuzzy_score(query: str, target: str) -> float:
    """Return a 0-1 similarity score between *query* and *target*."""
    q, t = query.lower(), target.lower()
    if q == t:
        return 1.0
    if q in t:
        return 0.9 + (len(q) / len(t)) * 0.1
    return SequenceMatcher(None, q, t).ratio()


def fuzzy_match_templates(
    query: str, templates: list[dict[str, str]], threshold: float = 0.55
) -> list[dict[str, str]]:
    """Return templates matching *query*, best match first.

    Exact substring matches are always included.  Fuzzy matches above
    *threshold* fill the rest.
    """
    scored: list[tuple[float, dict[str, str]]] = []
    for t in templates:
        score = _fuzzy_score(query, t["name"])
        if score >= threshold:
            scored.append((score, t))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [t for _, t in scored]


def _numbered_menu(items: list[str], prompt_text: str) -> int:
    """Display a numbered list and return the selected index."""
    click.echo("")
    for i, item in enumerate(items, 1):
        click.echo(f"  {Fore.CYAN}{i:>3}{Style.RESET_ALL}  {item}")
    click.echo("")
    while True:
        raw = click.prompt(prompt_text, type=str)
        try:
            idx = int(raw) - 1
            if 0 <= idx < len(items):
                return idx
        except ValueError:
            matches = [
                (i, item) for i, item in enumerate(items) if raw.lower() in item.lower()
            ]
            if len(matches) == 1:
                return matches[0][0]
            elif len(matches) > 1:
                click.echo(f"  Multiple matches for '{raw}':")
                for i, item in matches:
                    click.echo(f"    {i + 1}: {item}")
                continue
        click.echo(f"  Invalid selection. Enter 1-{len(items)} or a search term.")


def prompt_credentials() -> tuple[str, str]:
    access_id = click.prompt("WSU AccessID")
    password = getpass("Password: ")
    return access_id, password


def prompt_template(templates: list[dict[str, str]]) -> dict[str, str]:
    names = [t["name"] for t in templates]
    idx = _numbered_menu(names, "Select a building/template (number or search)")
    return templates[idx]


MAX_DAYS_AHEAD = 11


def prompt_date() -> str:
    today = date.today()
    max_date = today + timedelta(days=MAX_DAYS_AHEAD)
    default = today.strftime("%m/%d/%Y")

    while True:
        raw = click.prompt("Date (MM/DD/YYYY)", default=default)
        try:
            parsed = datetime.strptime(raw, "%m/%d/%Y").date()
        except ValueError:
            click.echo(f"  {Fore.RED}Invalid format. Use MM/DD/YYYY.{Style.RESET_ALL}")
            continue

        if parsed < today:
            click.echo(f"  {Fore.RED}Date cannot be in the past.{Style.RESET_ALL}")
            continue
        if parsed > max_date:
            click.echo(
                f"  {Fore.RED}EMS only allows bookings up to {MAX_DAYS_AHEAD} days "
                f"ahead (by {max_date.strftime('%m/%d/%Y')}).{Style.RESET_ALL}"
            )
            continue

        return raw


_TIME_RE = re.compile(r"^\s*(\d{1,2}):(\d{2})\s*(AM|PM|am|pm|a\.m\.|p\.m\.)?\s*$")


def _validate_time(raw: str) -> str | None:
    """Return the cleaned time string if valid, else None."""
    m = _TIME_RE.match(raw)
    if not m:
        return None
    hour, minute = int(m.group(1)), int(m.group(2))
    meridiem = m.group(3)
    if meridiem:
        if hour < 1 or hour > 12 or minute > 59:
            return None
    else:
        if hour > 23 or minute > 59:
            return None
    return raw.strip()


def prompt_start_time() -> str:
    while True:
        raw = click.prompt("Start time (e.g. 5:00 PM)")
        cleaned = _validate_time(raw)
        if cleaned:
            return cleaned
        click.echo(
            f"  {Fore.RED}Invalid time format. "
            f"Use H:MM AM/PM (e.g. 5:00 PM).{Style.RESET_ALL}"
        )


def prompt_end_time() -> str:
    while True:
        raw = click.prompt("End time (e.g. 6:00 PM)")
        cleaned = _validate_time(raw)
        if cleaned:
            return cleaned
        click.echo(
            f"  {Fore.RED}Invalid time format. "
            f"Use H:MM AM/PM (e.g. 6:00 PM).{Style.RESET_ALL}"
        )


def prompt_room(rooms: list[dict[str, Any]]) -> dict[str, Any]:
    names = [r["name"] for r in rooms]
    idx = _numbered_menu(names, "Select a room (number or search)")
    return rooms[idx]


def prompt_attendees() -> str:
    return click.prompt("Number of attendees", default="1")


def prompt_setup_type(setup_types: list[str]) -> str:
    idx = _numbered_menu(setup_types, "Select Setup Type (number or search)")
    return setup_types[idx]


def prompt_event_name() -> str:
    return click.prompt("Event Name")


def prompt_event_type(event_types: list[str]) -> str:
    idx = _numbered_menu(event_types, "Select Event Type (number or search)")
    return event_types[idx]


def prompt_contact_phone() -> str:
    return click.prompt("1st Contact Phone")


def prompt_contact_email() -> str:
    return click.prompt("1st Contact Email Address")


def prompt_av_technology() -> str:
    return click.prompt(
        "Will you be using the built-in audio/visual technology?",
        type=click.Choice(["Yes", "No"], case_sensitive=False),
        default="No",
    )


def prompt_event_description() -> str:
    return click.prompt("Please provide a detailed description of your event")


def prompt_event_time() -> str:
    return click.prompt("What is the actual event time?")


def prompt_sms_code() -> str:
    return click.prompt("Enter the verification code sent to your phone")


def prompt_confirm(message: str = "Proceed?") -> bool:
    return click.confirm(message, default=True)
