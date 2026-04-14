"""Setup configuration for warrior-bot."""

from setuptools import find_packages, setup

setup(
    name="warrior-bot",
    version="0.2.2",
    packages=find_packages(),
    package_data={
        "warrior_bot": ["commands/where/data/*.json", "data/*.json"],
    },
    install_requires=[
        "beautifulsoup4",
        "click",
        "colorama",
        "InquirerPy",
        "playwright",
        "requests",
    ],
    entry_points={
        "console_scripts": [
            "warrior-bot=warrior_bot.cli:cli",
            "wb=warrior_bot.cli:cli",
        ],
    },
    python_requires=">=3.10",
)
