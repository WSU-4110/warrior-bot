# where command

Find buildings, staff, and restaurants at Wayne State University.

## Usage
```bash
wb where <query>
wb where [OPTIONS] <query>
```

## Options

| Flag | Long Form | Description |
|------|-----------|-------------|
| `-b` | `--building` | Search for a building address |
| `-s` | `--staff` | Search for a staff or faculty member |
| `-r` | `--restaurants` | List on-campus and nearby restaurants |
| `-e` | `--email` | Open your mail app with the staff member's email (use with `-s`) |
| | `--campus` | On-campus dining only (use with `-r`) |
| | `--awd` | Anthony Wayne Drive restaurants only (use with `-r`) |

## Examples
```bash
# Find a staff or faculty member
wb where -s Naresh Mahabir

# Find a building address
wb where -b State Hall

# List all restaurants (23 locations)
wb where -r

# On-campus dining only
wb where -r --campus

# Anthony Wayne Drive restaurants only
wb where -r --awd

# Open mail app for a staff member
wb where -s Naresh Mahabir -e
```

## Search Types

- **Staff/Faculty**: Returns name, title, department, email, office location, and profile link
- **Buildings**: Returns the address and type of a WSU campus building (supports fuzzy matching)
- **Restaurants**: Lists dining options with address, phone, type, and description
