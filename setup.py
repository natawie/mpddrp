import setuptools;
import os;

with open("README.md", "r") as fh:
    long_description = fh.read();

setuptools.setup(
        name='mpddrp',
        version='1.0.1',
        packages=['mpddrp'],
        author="Franz Łotocki",
        author_email="flotocki002@gmail.com",
        description="MPD Discord Rich Presence",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/PanKohnih/mpddrp",
        install_requires=("python-mpd2", "pypresence"),
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
            "Operating System :: OS Independent"
        ],
)
