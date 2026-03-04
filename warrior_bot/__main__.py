import shlex
import sys

from warrior_bot.cli import cli
from warrior_bot.screens import title
from warrior_bot.screens import exit_screen

def repl() -> None:
    title.main(pause=False) #If we want to pause it as an 'Enter Press Start' Thing
    print("Warrior Bot CLI (interactive)")
    print("Type 'help' to see commands, 'exit' to quit.\n")

    while True:
        try:
            line = input("warrior-bot> ").strip()
        except (EOFError, KeyboardInterrupt):
            exit_screen.main(style="fancy", pause=False)
            return

        if not line:
            continue

        if line.lower() in {"exit", "quit"}: #Exit or Quit will close the program
            exit_screen.main(style="fancy", pause=False)
            return

        args = shlex.split(line)

        try:
            cli.main(args=args, prog_name="warrior-bot", standalone_mode=False)
        except SystemExit:
            pass
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        cli()
    else:
        repl()