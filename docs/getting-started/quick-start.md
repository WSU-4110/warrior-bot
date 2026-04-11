# Quick Start

This guide will get you up and running with warrior-bot in minutes.

## Basic Usage

warrior-bot (or `wb` for short) provides several commands to help you navigate WSU resources.

### Finding Staff or Faculty

Use the `where` command with the `-s` flag to find a staff or faculty member:
```bash
wb where -s Naresh Mahabir
```

### Finding a Building

Use the `-b` flag to search for a building address:
```bash
wb where -b State Hall
```

### Finding Restaurants

Use the `-r` flag to list on-campus and nearby dining options:
```bash
wb where -r
wb where -r --campus
wb where -r --awd
```

### Navigating to Resources

Use the `go` command to quickly access WSU resources:
```bash
wb go degree works
```

### Booking Facilities

Use the `book` command to reserve spaces:
```bash
wb book
```

## Command Aliases

You can use either the full command name or the short alias:
- `warrior-bot` or `wb`

Both work exactly the same way!

## Getting Help

For any command, you can add `--help` to see available options:
```bash
wb --help
wb go --help
wb where --help
wb book --help
```

## Next Steps

- Learn more about each [command](../commands/index.md)
- Check out the [development guide](../development/contributing.md) if you want to contribute
