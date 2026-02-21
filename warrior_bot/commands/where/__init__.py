"""Where command implementation."""


import click
import requests
from bs4 import BeautifulSoup

@click.command()
@click.argument("first_name")
@click.argument("last_name")
def where(first_name, last_name):
    """Where command."""

    click.echo("Executing where command...")

    url = f"https://wayne.edu/people?type=people&q={first_name}+{last_name}"

    response = requests.get(url)
    soup = BeautifulSoup(response.text,"html.parser")


    instructors = [row.find("td").get_text(strip=True)
                   for row in soup.select("table.table-stack tbody tr")]

    if not instructors:
        click.echo("No Instructor Found. Possible Issues: "
                   "\n - Incorrect Spelling"
                   "\n - Instructor may be new"
                   "\n - Instructor may be a Teacher Assistant"
                   "\n Please try again using wb where")
        return

    count = len(instructors)
    if count == 1:
        click.echo("Placeholder to avoid error")
        #Call the display info function
    else:
        #Could change to allow the user to select instructor directly
        click.echo(f"{count} instructors found. Please insert the name using wb where")
        for instructor in instructors:
            click.echo(f" - {instructor}")

    """End code for where command for Finding Instructors"""





#Additional Functions for more simple code
#def displayInstructorInfo(first_name,last_name,soup):
