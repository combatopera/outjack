# outjack
JACK and PortAudio integration for Python

## Install
These are generic installation instructions.

### To use, disposably
Install the current release from PyPI to a virtual environment:
```
python3 -m venv venvname
venvname/bin/pip install -U pip
venvname/bin/pip install outjack
. venvname/bin/activate
```

### To use, permanently
```
pip3 install --user outjack
```
See `~/.local/bin` for executables.

### To develop
First install venvpool to get the `motivate` command:
```
pip3 install --user venvpool
```
Get codebase and install executables:
```
git clone git@github.com:combatopera/outjack.git
motivate outjack
```
Requirements will be satisfied just in time, using sibling projects with matching .egg-info if any.

## Commands

### ojplay
Usage example.

## API

<a id="outjack.jackclient"></a>

### outjack.jackclient

<a id="outjack.portaudioclient"></a>

### outjack.portaudioclient

