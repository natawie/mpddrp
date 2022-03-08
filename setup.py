import sys
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

version = sys.version_info[:2]

if version < (3, 8):
    print("mpddrp uses pypresence which requires Python 3.8 or higher but Python {}.{} was detected. Please update!".format(*version))
    sys.exit(-1)

setup(
    name='mpddrp',
    version='1.1.2',
    packages=['mpddrp'],
    author="Natalia Łotocka",
    author_email="flotocki002@gmail.com",
    description="MPD Discord Rich Presence",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AKurushimi/mpddrp",
    install_requires=("python-mpd2", "pypresence", "colorama"),
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Intended Audience :: End Users/Desktop"
    ],
    entry_points={
        'console_scripts': [
            'mpddrp = mpddrp.main:main',
        ],
    },
)
