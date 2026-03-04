"""Where command implementation."""

import sys
import time

import click
import requests
from bs4 import BeautifulSoup


@click.command()
@click.argument("first_name")
@click.argument("last_name")
def where(first_name, last_name):
    """Where command Here is how to use:"""

    startTime = time.time()
    first_name = first_name.capitalize()
    last_name = last_name.capitalize()

    click.echo(f"Finding {first_name} {last_name}", nl=False)

    # just for fun. Not necessary for code to function. Still working on it a bit
    for _ in range(3):
        # click.echo(".",nl = False)
        sys.stdout.write(".")
        sys.stdout.flush()
        time.sleep(0.7)

    url = f"https://wayne.edu/people?type=people&q={first_name}+{last_name}"

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    staff = [
        row.find("td").get_text(strip=True)
        for row in soup.select("table.table-stack tbody tr")
    ]

    if not staff:
        click.echo("\r" + " " * 50 + "\r", nl=False)
        click.echo(
            "\033[31m[ERROR] No information on this staff member Found!\033[0m"
            "\n Possible Issues: "
            "\n - Incorrect Spelling"
            "\n - Instructor may be new"
            "\n - Instructor may be a Teacher Assistant"
            "\n Please try again using wb where"
        )
        click.echo(f"Command took {round(time.time() - startTime, 2)} seconds")
        return

    count = len(staff)
    if count == 1:
        click.echo("\r" + " " * 50 + "\r", nl=False)
        click.echo(displayStaffInfo(first_name, last_name, soup))
    else:
        click.echo("\r" + " " * 50 + "\r", nl=False)
        # Could change to allow the user to select instructor directly
        click.echo(f"{count} instructors found. Please insert the name using wb where")
        for name in staff:
            click.echo(f" - {name}")

    """End code for where command for Finding Instructors"""
    click.echo(f"Command took {round(time.time() - startTime, 2)} seconds")


# Additional Functions for more simple code
def displayStaffInfo(first_name, last_name, soup):

    RED = "\033[31m"
    RESET = "\033[0m"

    infoString = f"{first_name} {last_name} "
    errorString = ""

    row = soup.select_one("table.table-stack tbody tr")
    col = row.findAll("td")

    title = col[1].get_text(strip=True)
    dept = col[2].get_text(strip=True)
    phone = col[3].get_text(strip=True)
    email = col[4].get_text(strip=True)

    if title:
        infoString += f"has the title {title} and \n"

    if dept:
        infoString += (
            f"works in the {dept} department. \nYou can find them at PLACEHOLDER.\n"
        )
    else:
        errorString += (
            RED + "[ERROR] This staff member does not have a department.\n" + RESET
        )

    if email:
        infoString += f"Their email is {email}.\n"
    else:
        errorString += (
            RED
            + "[ERROR] This staff member does not have a registered email.\n"
            + RESET
        )

    if phone:
        infoString += f"Their phone number is {phone}.\n"
    else:
        errorString += (
            RED
            + "[ERROR] This staff member does not have a registered phone number.\n"
            + RESET
        )

    nameCol = col[0]
    linkTag = nameCol.find("a")
    if linkTag and linkTag.get("href"):
        link = "https://wayne.edu" + linkTag["href"]
        infoString += (
            f"For more information on {first_name} {last_name},"
            f" visit their web page: {link}\n"
        )
    else:
        errorString += (
            RED + "[ERROR] This staff member does not have a web page link.\n" + RESET
        )

    return infoString + errorString
