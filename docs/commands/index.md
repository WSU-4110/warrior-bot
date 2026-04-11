# warrior-bot

<img src="https://upload.wikimedia.org/wikipedia/commons/8/82/Wayne_State_Warriors_primary_logo.svg" width="128" height="128"/>

## Welcome!

warrior-bot is a CLI tool for Wayne State University staff and students. The idea is to make many of the things we need day to day easier to access and use through the terminal.

## Quick Start

Install warrior-bot by cloning the repo and running:
```bash
git clone https://github.com/WSU-4110/warrior-bot.git
cd warrior-bot
pip install -e .
```

Use the CLI:

"wb" is a shorthand alias for "warrior-bot"
```bash
# Find a staff member
wb where -s Naresh Mahabir

# Find a building
wb where -b State Hall

# Navigate to resources
wb go degree works

# Book a room
wb book state hall
```

## Next Steps

- [Installation Guide](getting-started/installation.md)
- [Quick Start Tutorial](getting-started/quick-start.md)
- [Command Reference](commands/index.md)

## License

This project is dual-licensed under MIT or Apache 2.0 - choose whichever works best for you.
