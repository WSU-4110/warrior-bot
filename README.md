# <img src="https://upload.wikimedia.org/wikipedia/commons/8/82/Wayne_State_Warriors_primary_logo.svg" width="32" height="32" style="vertical-align:middle;"/> warrior-bot
Terminal assistant for Wayne State University students.

## Welcome!
warrior-bot is a CLI tool for Wayne State University staff and students. The idea is to make many of the things we need day to day easier to
access and use through the terminal.

You can access the documentation [here](wsu-4110.github.io/warrior-bot/). 

Otherwise, some quick setup steps can be found below.

## Requirements
- Python 3.10+
- Access to a terminal
  - Recommended
    - [Ghostty](https://ghostty.org/)
    - [Alacritty](https://alacritty.org/)
    - [Kitty](https://sw.kovidgoyal.net/kitty/binary/)
    - [WezTerm](https://wezterm.org/index.html)

If you're on MacOS, we recommend [iTerm2](https://iterm2.com/)

## Setup (development)
Ensure you have a version of [Python](https://www.python.org/downloads/) >= 3.10 installed on your machine.

#### **Virtual Environment**
It's best that you use a [virtual environment](https://docs.python.org/3/library/venv.html) to both develop and test warrior-bot.

```bash
python3 -m venv venv # create virtual environment named "venv"

source venv/bin/activate # activate the virtual environment

pip install -r requirements.txt # install all needed libraries to your virtual environment

deactivate # deactivate the environment
```
#### **Install and run the CLI script**
To install the warrior-bot console script, run from root:
```bash
pip install -e .
```

Then, you can begin testing/iterating and developing on warrior-bot:
```bash
warrior-bot where naresh mahabir

wb go degree works

wb book --b state hall
```

#### **pre-commit hooks**
As a developer, you can install hooks to automatically do things like run `black`, `isort` or `flake8` on your files before they get committed.

To configure this, we already provide you with a `.pre-commit-config.yaml` file which will set this up for you. Simply run:

```bash
pip install -r requirements-dev.txt # install developer requirements

pre-commit install # install pre-commit cookes
```

Now, whenever you make some changes to your files, these hooks will automatically clean your code up for you or warn you when something looks out of place and allow you to adjust the files before pushing them upstream.

## License

This project is licensed under your choice of either:

- MIT License ([LICENSE-MIT](LICENSE-MIT))
- Apache License, Version 2.0 ([LICENSE-APACHE](LICENSE-APACHE))

You may choose either license to govern your use of this software.
