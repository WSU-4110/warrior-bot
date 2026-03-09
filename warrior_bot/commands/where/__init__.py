"""Where command implementation."""

import sys
import threading
import time

import click
import requests
from bs4 import BeautifulSoup


@click.command()
@click.argument("name", nargs = -1)
@click.option("-building", "-b", is_flag=True)
def where(name, building):
    """Where command."""

    fullName = " ".join(name).title()
    startTime = time.time()

    click.echo(f"Finding {fullName}", nl= False)

    #updated animation calls function later in file
    stop = threading.Event()
    animation = threading.Thread(target = loadingAnimation, args=(stop,))
    animation.start()

    if building:
        strategy = BuildingSearch(name, fullName, animation, stop)
        strategy.runBuildingSearch()
    else:
        strategy = StaffSearch(name, fullName, animation, stop)
        strategy.runStaffSearch()

    click.echo(f"Command took {round(time.time() - startTime,2)} seconds")

class StaffSearch:
    def __init__(self,name, fullName, animation, stop):
        self.name = name
        self.fullName = fullName
        self.animation = animation
        self.stop = stop

    def runStaffSearch(self):
        url = f"https://wayne.edu/people?type=people&q={"+".join(self.name).title()}"

        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.RequestException as e:
            click.echo("\r" + " " * 50 + "\r", nl = False)
            click.echo("\033[31m[ERROR] Could not gain access to URL\033[0m")
            return

        soup = BeautifulSoup(response.text,"html.parser")

        staff = [row.find("td").get_text(strip=True)
                 for row in soup.select("table.table-stack tbody tr")]

        if not staff:
            self.stop.set()
            self.animation.join()
            click.echo("\r" + " " * 50 + "\r", nl = False)
            click.echo("\033[31m[ERROR] No information on this staff member found!\033[0m"
                       "\n Possible Issues: "
                       "\n - Incorrect Spelling"
                       "\n - Instructor may be new"
                       "\n - Instructor may be a Teacher Assistant"
                       "\n For building use -building ot -b after the name"
                       "\n Please try again using wb where")
            return

        count = len(staff)
        if count == 1:
            self.stop.set()
            self.animation.join()
            click.echo("\r" + " " * 50 + "\r", nl = False)
            click.echo(self.displayStaffInfo(self.fullName, soup))
        else:
            self.stop.set()
            self.animation.join()
            click.echo("\r" + " " * 50 + "\r", nl = False)
            #Could change to allow the user to select instructor directly
            click.echo(f"{count} instructors found. Please insert the name using wb where")
            for name in staff:
                click.echo(f" - {name}")

        """End code for where command for Finding Instructors"""

    def displayStaffInfo(self,fullName, soup):

            RED = "\033[31m"
            RESET = "\033[0m"

            infoString = f"{fullName} "
            errorString = ""

            row = soup.select_one("table.table-stack tbody tr")
            col = row.findAll("td")

            title = col[1].get_text(strip=True)
            dept = col[2].get_text(strip=True)
            phone = col[3].get_text(strip=True)
            email = col[4].get_text(strip=True)

            if title:
                infoString += f"has the title {title} and \n"

            if dept:
                infoString += (
                    f"works in the {dept} department. \nYou can find them at PLACEHOLDER.\n"
                )
            else:
                errorString += (
                        RED + "[ERROR] This staff member does not have a department.\n" + RESET
                )

            if email:
                infoString += f"Their email is {email}.\n"
            else:
                errorString += (
                        RED
                        + "[ERROR] This staff member does not have a registered email.\n"
                        + RESET
                )

            if phone:
                infoString += f"Their phone number is {phone}.\n"
            else:
                errorString += (
                        RED
                        + "[ERROR] This staff member does not have a registered phone number.\n"
                        + RESET
                )

            nameCol = col[0]
            linkTag = nameCol.find("a")
            if linkTag and linkTag.get("href"):
                link = "https://wayne.edu" + linkTag["href"]
                infoString += f"For more information on {fullName}, visit their web page: {link}\n"
            else:
                errorString += (
                        RED + "[ERROR] This staff member does not have a web page link.\n" + RESET
                )

            return infoString + errorString

class BuildingSearch:
    def __init__(self,name, fullName, animation, stop):
        self.name = name
        self.fullName = fullName
        self.animation = animation
        self.stop = stop
    def runBuildingSearch(self):
        self.stop.set()
        self.animation.join()
        click.echo("\r" + " " * 50 + "\r", nl = False)
        url = "https://maps.wayne.edu/all/" #maybe use this
        click.echo("Flagged as Building..."
                   "\nThis Feature is currently non-functional."
                   f"\nFor building information go to {url}")
        #this will read from a json file and return results.
        # could also be called in displayStaffInfo to tell users where to find a person

#animation function
def loadingAnimation(stop):
    while not stop.is_set():
        for _ in range(3):
            sys.stdout.write(".")
            sys.stdout.flush()
            time.sleep(0.7)
        sys.stdout.write("\b" * 3 + " " * 3 + "\b" * 3)
        sys.stdout.flush()

