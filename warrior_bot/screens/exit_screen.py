from abc import ABC, abstractmethod
import os
from colorama import Fore, Style, init
init(autoreset=True)

class ExitScreen(ABC):
    @abstractmethod
    def display(self):
        pass


class SimpleExit(ExitScreen):
    def display(self):
        print("=== THANKS FOR USING WARRIOR-BOT ===")


class FancyExit(ExitScreen):
    def display(self):
        print(Fore.GREEN + r"""
 ██████╗  ██████╗  ██████╗ ██████╗     ██████╗ ██╗   ██╗███████╗██╗
██╔════╝ ██╔═══██╗██╔═══██╗██╔══██╗    ██╔══██╗╚██╗ ██╔╝██╔════╝██║
██║  ███╗██║   ██║██║   ██║██║  ██║    ██████╔╝ ╚████╔╝ █████╗  ██║
██║   ██║██║   ██║██║   ██║██║  ██║    ██╔══██╗  ╚██╔╝  ██╔══╝  ╚═╝
╚██████╔╝╚██████╔╝╚██████╔╝██████╔╝    ██████╔╝   ██║   ███████╗██╗
 ╚═════╝  ╚═════╝  ╚═════╝ ╚═════╝     ╚═════╝    ╚═╝   ╚══════╝╚═╝

   === THANKS FOR USING WARRIOR BOT ===
        """ + Style.RESET_ALL)


class ExitFactory:
    @staticmethod
    def create_exit(style: str):
        if style.lower() == "simple":
            return SimpleExit()
        elif style.lower() == "fancy":
            return FancyExit()
        else:
            raise ValueError("Unknown style type.")


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def main(style: str = "fancy", pause: bool = False):
    clear_screen()
    screen = ExitFactory.create_exit(style)
    screen.display()
    if pause:
        input("\nPress Enter to close...")