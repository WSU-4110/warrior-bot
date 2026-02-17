"""Where command implementation."""

import click
import requests
from bs4 import BeautifulSoup

@click.command()
@click.argument("name")
def where(name):
    """Where command."""

    click.echo("Executing where command")

    url = f"https://wayne.edu/people?type=people&q={name.replace(' ','+')}"

    response = requests.get(url)
    soup = BeautifulSoup(response.text,"html.parser")

    instructors = soup.find_all("td",{"data-label": "Name"})

    if not instructors:
        click.echo("No Instructor Found. Possible Issues: "
                   "\n - Incorrect Spelling"
                   "\n - Instructor may be new"
                   "\n - Instructor may be a Teacher Assistant"
                   "\n Please try again using wb where")
        return



    click.echo("Executing where command")
