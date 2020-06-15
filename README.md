# mpddrp
mpddrp is a simple python script that displays what you're currently listening to through MPD on Discord.
## Requirements
* [pypresence](https://github.com/qwertyquerty/pypresence)
* [python-mpd2](https://github.com/Mic92/python-mpd2)
## How to run
If you don't know a thing about python here's what you do:
### Windows(not tested)
* Install the newest version of [Python 3.*](https://www.python.org/downloads/)
* In the Powershell install dependencies by typing:
```powershell
pip install pypresence
pip install python-mpd2
```
* `cd` into the location with the script
* Then type: ```python3 mpddrp.py```
### Linux
* Install ```python3``` using the package manager you have with your distribution(if it's not preinstalled):
> Debian-based distros(Debian, Ubuntu, Mint, etc.)
```bash
sudo apt-get install python3 python-pip
```
> Arch-based distros(Arch, Manjaro, Artix etc.)
```bash
sudo pacman -S python3 python-pip
```
* Install dependencies by typing:
```bash
sudo pip3 install pypresence
sudo pip3 install python-mpd2
```
* ```cd``` into the location with the script
* Then type: ```python3 mpddrp.py```
### MacOs(not tested)
* Install [homebrew](https://brew.sh/)
* Install python by typing:
```zsh
brew install python
```
* Install dependencies by typing:
```zsh
sudo pip3 install pypresence
sudo pip3 install python-mpd2
```
* ```cd``` into the location with the script
* Then type: ```python3 mpddrp.py```
