# book command

Reserve rooms and spaces at Wayne State University through EMS.

## Usage
```bash
wb book <building>
```

## Examples
```bash
# Book a room in State Hall
wb book state hall

# Book a room in STEM
wb book stem

# Book a lounge space
wb book lounge space

# Debug mode (shows browser window)
wb book state hall --headed
```

## Available Buildings

| Building | Description |
|----------|-------------|
| `state hall` | Reserve a room in State Hall |
| `stem` | Reserve a room in STEM |
| `lounge space` | Reserve a lounge space room |

## Options

| Flag | Description |
|------|-------------|
| `--headed` | Show the browser window for debugging |

Use `--help` to see all available options:
```bash
wb book --help
```
