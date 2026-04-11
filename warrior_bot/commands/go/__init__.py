"""Go command implementation."""

import difflib
import webbrowser

import click


class URL_Command:
    def __init__(self, name, url):
        self.name = name
        self.url = url

    def execute(self):
        click.echo("Executing go command.")
        try:
            success = webbrowser.open(self.url, new=1, autoraise=True)
            if not success:
                click.echo("ERROR: Could not access local browser.")
        except Exception:
            click.echo("ERROR: Could not access local browser.")


commands = {
    "academica": URL_Command("WSU Academica", "https://academica.aws.wayne.edu/"),
    "library": URL_Command("WSU Library", "https://library.wayne.edu/"),
    "bookstore": URL_Command("WSU Bookstore", "https://waynestatebookstore.com/"),
    "degreeworks": URL_Command("WSU Degree Works", "https://degreeworks.wayne.edu/"),
}


@click.command()
@click.argument("resource", nargs=-1)
@click.pass_context
def go(ctx, resource):
    """Open a supported WSU website.

    \b
    RESOURCES:
      academica   - WSU Academica
      library     - WSU Library
      bookstore   - WSU Bookstore
      degreeworks - Degree Works (accepts "degree works")
    """
    if not resource:
        click.echo(ctx.get_help())
        ctx.exit()

    text = " ".join(resource).lower().strip()

    if text == "help":
        click.echo(ctx.get_help())
        ctx.exit()

    cmd = commands.get(text)
    if cmd is None:
        cmd = commands.get(text.replace(" ", ""))
    if cmd:
        cmd.execute()
    else:
        lookup = text.replace(" ", "")
        matches = difflib.get_close_matches(lookup, commands.keys(), n=1)
        if matches:
            click.echo(f"Invalid resource -- did you mean '{matches[0]}'?")
        else:
            click.echo("Invalid resource.")
            click.echo("Available resources: " + ", ".join(commands.keys()))
