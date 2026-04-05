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


class goHelpCommand(click.Command):  # Help command information
    def format_help(self, ctx, formatter):
        formatter.write_text("Go Command: Open a supported WSU website.")
        formatter.write_paragraph()

        formatter.write_text("Usage: wb go [RESOURCE]")
        formatter.write_paragraph()

        formatter.write_text("RESOURCES:")
        formatter.write_text(
            "  academica - Opens your browser to the Academica website."
        )
        formatter.write_text(
            "  library  -  Opens your browser to the WSU Library website."
        )
        formatter.write_text(
            "  bookstore - Opens your browser to the WSU Bookstore website."
        )
        formatter.write_text("  help or --help - Show this message")
        formatter.write_paragraph()

        formatter.write_text("Help Menu:")
        formatter.write_text("  wb help or wb --help")


@click.command()
@click.argument("resource")
def go(resource):
    resource = resource.lower()
    cmd = commands.get(resource)
    if cmd:
        cmd.execute()
    else:
        matches = difflib.get_close_matches(resource, commands.keys(), n=1)
        if matches:
            click.echo(f"Invalid resource -- did you mean '{matches[0]}'?")
        else:
            click.echo("Invalid resource.")
            click.echo("Available resources: " + ", ".join(commands.keys()))
