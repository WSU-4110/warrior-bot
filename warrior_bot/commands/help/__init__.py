import click


def showHelp(ctx: click.Context, value: str | None) -> None:
    if value is None or value.lower() == "help":
        click.echo(ctx.get_help())
        ctx.exit()


def mainHelp(formatter) -> None:
    formatter.write_text(
        "Warrior Bot: Your campus companion for navigating Warrior life."
    )
    formatter.write_paragraph()

    formatter.write_text("Usage: wb [COMMAND] [OPTIONS]")
    formatter.write_paragraph()

    formatter.write_text("COMMANDS:")
    formatter.write_text("  go    - Open supported WSU websites")
    formatter.write_text("  where - Find faculty, building, and restaurant information")
    formatter.write_text("  book  - Reserve rooms on EMS")
    formatter.write_text("  help  - Show this message")
    formatter.write_paragraph()

    formatter.write_text("HELP:")
    formatter.write_text("  wb help")
    formatter.write_text("  wb --help")
    formatter.write_text("  wb go help")
    formatter.write_text("  wb where help")
    formatter.write_text("  wb book help")


@click.command(name="help")
@click.pass_context
def help(ctx: click.Context) -> None:

    from warrior_bot.cli import BANNER

    click.echo(BANNER)
    formatter = ctx.make_formatter()
    mainHelp(formatter)
    click.echo(formatter.getvalue())


class goHelpCommand(click.Command):
    def format_help(self, ctx, formatter):
        formatter.write_text("Usage: wb go RESOURCE")
        formatter.write_paragraph()

        formatter.write_text("Go Command: Open a supported WSU website.")
        formatter.write_paragraph()

        formatter.write_text("RESOURCES:")
        formatter.write_text(
            "  academica - Opens your browser to the Academica website"
        )
        formatter.write_text(
            "  library - Opens your browser to the WSU Library website"
        )
        formatter.write_text(
            "  bookstore - Opens your browser to the WSU Bookstore website"
        )
        formatter.write_text("  help or --help - Show this message")
        formatter.write_paragraph()

        formatter.write_text("Help Menu:")
        formatter.write_text("  wb help or wb --help")


class whereHelpCommand(click.Command):
    def format_help(self, ctx, formatter):
        formatter.write_text("Usage: wb where RESOURCE")
        formatter.write_paragraph()

        formatter.write_text(
            "Where Command: Finds faculty, building, and restaurant information."
        )
        formatter.write_paragraph()

        formatter.write_text("RESOURCES:")
        formatter.write_text("  professor name - Search for a faculty member")
        formatter.write_text("  -building or -b - Search for building-related info")
        formatter.write_text("  -restaurants or -r - Search for on-campus restaurants")
        formatter.write_text("    --campus - On-campus dining only")
        formatter.write_text("    --awd   - Anthony Wayne Drive only")
        formatter.write_text("  help or --help - Show this message")
        formatter.write_paragraph()

        formatter.write_text("Help Menu:")
        formatter.write_text("  wb help or wb --help")


class bookHelpCommand(click.Command):
    def format_help(self, ctx, formatter):
        formatter.write_text("Usage: wb book BUILDING")
        formatter.write_paragraph()

        formatter.write_text("Book Command: Reserve rooms on EMS.")
        formatter.write_paragraph()

        formatter.write_text("RESOURCES:")
        formatter.write_text("  state hall - Reserve a room in State Hall")
        formatter.write_text("  stem - Reserve a room in STEM")
        formatter.write_text("  lounge space - Reserve a lounge space room")
        formatter.write_text("  help or --help - Show this message")
        formatter.write_paragraph()

        formatter.write_text("Help Menu:")
        formatter.write_text("  wb help or wb --help")
