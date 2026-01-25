# Architecture

warrior-bot is designed with a modular architecture that makes it easy to add new commands.

> AI Disclosure Notice:
> This document was generated using Claude Opus 4.5, and finely edited by a human.

## Project Structure

```
warrior-bot/
├── warrior_bot/           # Main package
│   ├── __init__.py       # Package initialization
│   ├── __main__.py       # Entry point for python -m
│   ├── cli.py            # CLI setup and command registration
│   └── commands/         # All commands
│       ├── go/
│       │   └── __init__.py
│       ├── where/
│       │   └── __init__.py
│       └── book/
│           └── __init__.py
├── docs/                 # Documentation
├── tests/               # Tests (coming soon)
├── setup.py            # Package setup
├── mkdocs.yml          # Documentation config
└── requirements.txt    # Dependencies
```

## Command Architecture

Each command lives in its own folder under `warrior_bot/commands/`. This provides:

- **Isolation**: Each command is self-contained
- **Scalability**: Easy to add complexity without affecting other commands
- **Clarity**: Clear separation of concerns

### Command Structure

Each command is a Click command function:

```python
import click

@click.command()
@click.option('--flag', is_flag=True, help='Example flag')
@click.argument('arg')
def mycommand(flag, arg):
    """Command description."""
    click.echo(f"Running with arg: {arg}")
```

### Command Registration

Commands are registered in `cli.py`:

```python
import click
from warrior_bot.commands import go, where, book

@click.group()
def cli():
    """Warrior Bot CLI."""
    pass

cli.add_command(go.go)
cli.add_command(where.where)
cli.add_command(book.book)
```

## Design Principles

1. **Keep it simple**: Commands should be straightforward to use
2. **Modular design**: Each command is independent
3. **Consistent UX**: All commands follow similar patterns
4. **Extensible**: Easy to add new commands and features

## Technology Stack

- **Click**: CLI framework
- **Python 3.10+**: Language and runtime
- **MkDocs Material**: Documentation
- **GitHub Actions**: CI/CD
