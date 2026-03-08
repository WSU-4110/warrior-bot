"""Go command implementation."""

import click
import webbrowser

class URL_Command:
    def __init__(self, name, url)P:
        self.url = url;
        self.name = name;
    def execute(self):
        click.echo("Executing go command.")
        click.echo("Taking user to {self.name}.")

@click.command()
@click.argument("resource")
def go(resource):
    """Go command."""
    click.echo("Executing go command")
    
    if resource == "academica":
        click.echo("Taking user to WSU Academica site!")
        url = 'http://academica.aws.wayne.edu/'
        webbrowser.open(url, new=1, autoraise=True)
    elif resource == "library":
        click.echo("Taking user to WSU Library site!")
        url = 'https://library.wayne.edu/'
        webbrowser.open(url, new=1, autoraise=True)
    elif resource == "bookstore":
        click.echo("Taking user to WSU Bookstore site!")
    else:
        click.echo("invalid command")
