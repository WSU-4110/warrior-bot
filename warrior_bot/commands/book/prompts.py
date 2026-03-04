"""Terminal prompt helpers for the book command using click (sync, no asyncio)."""

from datetime import date
from getpass import getpass
from typing import Any

import click
from colorama import Fore, Style


def _numbered_menu(items: list[str], prompt_text: str) -> int:
    """Display a numbered list and return the selected index."""
    click.echo("")
    for i, item in enumerate(items, 1):
        click.echo(f"  {Fore.CYAN}{i:>3}{Style.RESET_ALL}  {item}")
    click.echo("")
    while True:
        raw = click.prompt(prompt_text, type=str)
        # Allow searching by typing part of a name
        try:
            idx = int(raw) - 1
            if 0 <= idx < len(items):
                return idx
        except ValueError:
            # Search by substring
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


def prompt_date() -> str:
    default = date.today().strftime("%m/%d/%Y")
    return click.prompt("Date (MM/DD/YYYY)", default=default)


def prompt_start_time() -> str:
    return click.prompt("Start time (e.g. 5:00 PM)")


def prompt_end_time() -> str:
    return click.prompt("End time (e.g. 6:00 PM)")


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


def prompt_confirm(message: str = "Proceed?") -> bool:
    return click.confirm(message, default=True)
