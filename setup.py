from os import pipe
from setuptools import setup, find_packages

setup(
    name="five_timer",
    version = "v_1.0",
    description = "555-Timer calculator",
    author = "Edwin Mwiti",
    author_email = "emwiti658@gmail.com",
    url = "https://github.com/edwinmwiti/five-timer",
    install_requires = ['Pillow'],
    packages = find_packages(),

    package_data = {
        "five_timer": ["resources/*"]
    },
    entry_points = {
        "gui_scripts": ["five-timer = five_timer.main:initialize"]
    }
)
