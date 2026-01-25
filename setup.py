"""Setup configuration for warrior-bot."""

from setuptools import find_packages, setup

setup(
    name="warrior-bot",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "click",
    ],
    entry_points={
        "console_scripts": [
            "warrior-bot=warrior_bot.cli:cli",
            "wb=warrior_bot.cli:cli",
        ],
    },
    python_requires=">=3.10",
)
