import pathlib
from setuptools import setup

from weathercli import __app_name__, __version__

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name=__app_name__,
    version=__version__,
    description="A simple CLI to view current and forecast weather data in the terminal.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/carstenstann/weathercli/",
    author="Carsten Stann",
    author_email="cs.contact@tutanota.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    packages=["weathercli"],
    python_requires=">=3.6",
    include_package_data=True,
    install_requires=[],
    entry_points={"console_scripts": ["weather=weathercli.cli:cli"]},
)
