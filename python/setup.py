from setuptools import setup, find_packages


console_scripts = """
    [console_scripts]
    osm_wheelchair=osm_wheelchair.osm_wheelchair:cli
    """

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="osm_wheelchair",
    version="1.0",
    description="Install script for the osm_wheelchair package.",
    author="J.Keaflein, T.Schneider, J.Stier",
    author_email="stier.jochen@web.de",
    url="",
    packages=find_packages(exclude=("tests", "docs")),
    install_requires=requirements,
    entry_points=console_scripts,
)
