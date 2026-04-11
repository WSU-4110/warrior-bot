"""Where command implementation."""

import platform
import re
import subprocess
import sys
import threading
import time

import click

from warrior_bot.commands.where.where_facade import WhereFacade


@click.command()
@click.argument("name", nargs=-1)
@click.option(
    "-b",
    "--building",
    is_flag=True,
    help="Search for a building address.",
)
@click.option("-s", "--staff", is_flag=True, help="Search for a staff member.")
@click.option(
    "-r",
    "--restaurants",
    is_flag=True,
    help="List all on-campus and nearby restaurants.",
)
@click.option("--campus", is_flag=True, help="On-campus dining only (use with -r).")
@click.option(
    "--awd",
    is_flag=True,
    help="Anthony Wayne Drive only (use with -r).",
)
@click.option(
    "-e", "--email", is_flag=True, help="Open mail app with professor's email."
)
@click.pass_context
def where(ctx, name, building, staff, restaurants, campus, awd, email):
    """Find buildings, staff, and restaurants at Wayne State.

    \b
    EXAMPLES:
      wb where Panda Express    Search across everything
      wb where -s John Doe      Search for staff member
      wb where -b State Hall    Search for a building
      wb where -r               List all restaurants
      wb where -r --campus      On-campus dining only
    """
    if not name and not restaurants:
        click.echo(ctx.get_help())
        ctx.exit()

    if len(name) == 1 and name[0].lower() == "help":
        click.echo(ctx.get_help())
        ctx.exit()

    facade = WhereFacade()
    start_time = time.time()

    if restaurants:
        if name:
            query = " ".join(name)
            click.echo(f"Searching for restaurant: {query}", nl=False)
            stop, animation = _start_animation()
            result, _ = facade.search_restaurants_by_name(query)
            _stop_animation(stop, animation)
        elif awd:
            click.echo("Loading Anthony Wayne Drive restaurants", nl=False)
            stop, animation = _start_animation()
            result, _ = facade.search_restaurants(category="awd")
            _stop_animation(stop, animation)
        elif campus:
            click.echo("Loading on-campus dining locations", nl=False)
            stop, animation = _start_animation()
            result, _ = facade.search_restaurants(category="campus")
            _stop_animation(stop, animation)
        else:
            click.echo("Loading all restaurants", nl=False)
            stop, animation = _start_animation()
            result, _ = facade.search_restaurants(category="all")
            _stop_animation(stop, animation)
        click.echo(result)

    elif building:
        query = " ".join(name)
        if not query:
            click.echo(
                click.style(
                    "[ERROR] Provide a building name. e.g. wb where -b State Hall",
                    fg="red",
                )
            )
            ctx.exit()
        result, _ = facade.search_building(query)
        click.echo(result)

    elif staff:
        full_name = " ".join(name).title()
        click.echo(f"Finding {full_name}", nl=False)
        stop, animation = _start_animation()
        result, staff_data = facade.search_staff(full_name)
        _stop_animation(stop, animation)
        click.echo(result)

        if email:
            clean_result = re.sub(r"\x1b\[[0-9;]*m", "", result)
            match = re.search(
                r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", clean_result
            )
            professor_email = match.group(0) if match else None

            if professor_email:
                click.echo(f"Opening mail app for: {professor_email}")
                _open_mail(professor_email)
            else:
                click.echo(
                    click.style(
                        "[ERROR] No email found for this staff member.", fg="red"
                    )
                )
    else:
        query = " ".join(name).title()
        click.echo(f"Finding {query}", nl=False)
        stop, animation = _start_animation()
        result, found = facade.search_all(query)
        _stop_animation(stop, animation)
        click.echo(result)

        if found and email:
            clean_result = re.sub(r"\x1b\[[0-9;]*m", "", result)
            match = re.search(
                r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", clean_result
            )
            professor_email = match.group(0) if match else None

            if professor_email:
                click.echo(f"Opening mail app for: {professor_email}")
                _open_mail(professor_email)

    click.echo(f"Command took {round(time.time() - start_time, 2)} seconds")


def _start_animation() -> tuple[threading.Event, threading.Thread]:
    stop = threading.Event()
    animation = threading.Thread(target=_loading_animation, args=(stop,))
    animation.start()
    return stop, animation


def _stop_animation(stop: threading.Event, animation: threading.Thread) -> None:
    stop.set()
    animation.join()
    click.echo("\r" + " " * 50 + "\r", nl=False)


def _loading_animation(stop: threading.Event) -> None:
    while not stop.is_set():
        for _ in range(3):
            sys.stdout.write(".")
            sys.stdout.flush()
            time.sleep(0.7)
        sys.stdout.write("\b" * 3 + " " * 3 + "\b" * 3)
        sys.stdout.flush()


def _open_mail(email_address):
    mailto = f"mailto:{email_address}"

    system = platform.system()
    if system == "Darwin":
        subprocess.run(["open", mailto])
    elif system == "Windows":
        subprocess.run(["start", mailto], shell=True)
    else:
        subprocess.run(["xdg-open", mailto])


# Backward-compatible exports used by the test suite.
loadingAnimation = _loading_animation
stopAnimation = _stop_animation


def displayStaffInfo(name: str, soup) -> str:
    """Format a staff search result row from the legacy HTML table structure."""

    for row in soup.select("table.table-stack tbody tr"):
        cells = row.find_all("td")
        if not cells:
            continue

        link = cells[0].find("a")
        if link:
            staff_name = link.get_text(strip=True)
        else:
            staff_name = cells[0].get_text(strip=True)
        if staff_name != name:
            continue

        title = cells[1].get_text(strip=True) if len(cells) > 1 else ""
        department = cells[2].get_text(strip=True) if len(cells) > 2 else ""
        phone = cells[3].get_text(strip=True) if len(cells) > 3 else ""
        email = cells[4].get_text(strip=True) if len(cells) > 4 else ""
        profile_path = link.get("href", "") if link else ""

        if not any([title, department, phone, email]):
            return "[ERROR] No staff info found"

        profile_url = f"https://wayne.edu{profile_path}" if profile_path else ""
        parts = [staff_name]
        if title:
            parts.append(title)
        if department:
            parts.append(department)
        if phone:
            parts.append(phone)
        if email:
            parts.append(email)
        if profile_url:
            parts.append(profile_url)
        return "\n".join(parts)

    return "[ERROR] No staff info found"
