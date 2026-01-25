# Contributing

Thank you for your interest in contributing to warrior-bot!

## Development Setup

1. Clone the repository:

```bash
git clone https://github.com/yourusername/warrior-bot.git
cd warrior-bot
```

2. Create a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install development dependencies:

```bash
pip install -r requirements-dev.txt
pip install -e .
```

4. Set up pre-commit hooks:

```bash
pre-commit install
```

## Code Standards

We use several tools to maintain code quality:

- **black**: Code formatting
- **isort**: Import sorting
- **flake8**: Linting
- **mypy**: Type checking

Run all checks:

```bash
black warrior_bot/
isort warrior_bot/
flake8 warrior_bot/
mypy warrior_bot/
```

Or let pre-commit handle it automatically when you commit.

## Adding a New Command

1. Create a new folder in `warrior_bot/commands/`:

```bash
mkdir warrior_bot/commands/mycommand
```

2. Create `__init__.py` with your command:

```python
"""My command implementation."""

import click


@click.command()
def mycommand():
    """My command description."""
    click.echo("Hello from mycommand!")
```

3. Register it in `warrior_bot/cli.py`:

```python
from warrior_bot.commands import mycommand

# In the cli function:
cli.add_command(mycommand.mycommand)
```

## Documentation

Update the docs when adding features:

1. Edit files in the `docs/` directory
2. Preview locally:

```bash
mkdocs serve
```

3. Visit `http://127.0.0.1:8000` to see your changes

## Submitting Changes

1. Create a new branch:

```bash
git checkout -b feature/my-feature
```

2. Make your changes and commit:

```bash
git add .
git commit -m "Add my feature"
```

3. Push and create a pull request:

```bash
git push origin feature/my-feature
```

## Questions?

Feel free to open an issue if you have questions!
