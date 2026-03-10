"""Go command implementation."""

import click
import webbrowser

class URL_Command:
    def __init__(self, name, url):
        self.url = url;
        self.name = name;
    def execute(self):
        click.echo("Executing go command.")
        click.echo("Taking user to {self.name}!")
        webbrowser.open(self.url, new=1, autoraise=True)

commands = {
  "academica": URL_Command("WSU Academica", "https://academica.aws.wayne.edu/"),
  "library": URL_Command("WSU Library", "https://library.wayne.edu/"),
  "bookstore": URL_Command("WSU Bookstore", "https://waynestatebookstore.com/")
}

@click.command()
@click.argument("resource")
def go(resource):
    """Go command.""
    comd = commands.get(resource)
    if cmd:
        cmd.execute()
    else:
        click.echo("invalid command")
