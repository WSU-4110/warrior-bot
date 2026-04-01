"""Tests for the 'where' command."""

import pytest
from bs4 import BeautifulSoup
from click.testing import CliRunner

from warrior_bot.commands.where import (
    displayStaffInfo,
    loadingAnimation,
    stopAnimation,
    where,
)

"""Staff tests"""


# test link creating link
def test_create_url():
    # following code from where command
    name = ["First", "Last"]
    query = "+".join(name).title()
    url = f"https://wayne.edu/people?type=people&q={query}"
    assert "First+Last" in url


# test runtime of program
@pytest.mark.timeout(15)  # timeout based on non-functional requirements
def test_runtime():
    runner = CliRunner()
    result = runner.invoke(where, ["First", "Last"])

    assert result.exit_code == 0
    assert "[ERROR]" in result.output


# test HTML Parser with name
def test_html_parser():
    html = """
    <table class="table-stack">
        <tbody>
            <tr><td>First Last</td></tr>
        </tbody>
    </table>
    """

    # following code from where command
    soup = BeautifulSoup(html, "html.parser")
    staff = [
        row.find("td").get_text(strip=True)
        for row in soup.select("table.table-stack tbody tr")
    ]

    assert staff == ["First Last"]


# test displayStaffInfo with all info found
def test_display_all():
    html = """
    <table class="table-stack">
        <tbody>
            <tr>
            <td><a href="/profile/ab1234">First Last</a></td>
            <td>Title</td>
            <td>Department</td>
            <td>Phone</td>
            <td>Email</td>
            <td>Link</td>
            </tr>
        </tbody>
    </table>
    """

    soup = BeautifulSoup(html, "html.parser")
    result = displayStaffInfo("First Last", soup)

    assert "Title" in result
    assert "Department" in result
    assert "Email" in result
    assert "Phone" in result
    assert "https://wayne.edu" in result


# test displayStaffInfo with no info found
def test_display_errors():

    html = """
    <table class="table-stack">
        <tbody>
            <tr>
            <td><a href="/profile/ab1234">First Last</a></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            </tr>
        </tbody>
    </table>
    """

    soup = BeautifulSoup(html, "html.parser")
    result = displayStaffInfo("First Last", soup)

    assert "[ERROR]" in result


# Test Animation ends properly
def test_end_animation():
    import threading
    import time

    stop = threading.Event()
    animationTest = threading.Thread(target=loadingAnimation, args=(stop,))
    animationTest.start()
    time.sleep(5)
    stopAnimation(stop, animationTest)

    assert not animationTest.is_alive()


"""Location tests"""


# test building flag triggers building path
def test_building_flag():
    runner = CliRunner()
    result = runner.invoke(where, ["State", "Hall", "-building"])

    assert result.exit_code == 0
    assert "Flagged as Building" in result.output


# test building shorthand flag works
def test_building_shorthand_flag():
    runner = CliRunner()
    result = runner.invoke(where, ["State", "Hall", "-b"])

    assert result.exit_code == 0
    assert "Flagged as Building" in result.output


# test building path includes maps URL
def test_building_maps_url():
    runner = CliRunner()
    result = runner.invoke(where, ["State", "Hall", "-building"])

    assert "https://maps.wayne.edu/all/" in result.output


# test building path shows non-functional message
def test_building_nonfunctional_message():
    runner = CliRunner()
    result = runner.invoke(where, ["State", "Hall", "-b"])

    assert "non-functional" in result.output


# test building runtime within non-functional requirements
@pytest.mark.timeout(15)
def test_building_runtime():
    runner = CliRunner()
    result = runner.invoke(where, ["Engineering", "-b"])

    assert result.exit_code == 0
    assert "Command took" in result.output


# test building flag with single-word location name
def test_building_single_word():
    runner = CliRunner()
    result = runner.invoke(where, ["Library", "-b"])

    assert result.exit_code == 0
    assert "Flagged as Building" in result.output
    assert "https://maps.wayne.edu/all/" in result.output
