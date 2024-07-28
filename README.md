# Tempo120

[![License: BSD](https://img.shields.io/badge/License-GNU%20GPL-blue)](https://github.com/dkrajzew/tempo120/blob/master/LICENSE)
[![PyPI version](https://badge.fury.io/py/tempo120.svg)](https://pypi.python.org/pypi/tempo120)
[![Downloads](https://pepy.tech/badge/tempo120)](https://pepy.tech/project/tempo120)
[![Downloads](https://static.pepy.tech/badge/tempo120/week)](https://pepy.tech/project/tempo120)


A racing game written using Python/pygame during the [bpb](https://www.bpb.de/) ([Bundeszentrale für politische Bildung](https://www.bpb.de/)) [game jam 2023](https://www.bpb.de/veranstaltungen/veranstaltungskalender/518950/bpb-game-jam-2023/). The game jam's topic was mobility.

<!-- imgs begin -->
<img src="https://github.com/dkrajzew/tempo120/blob/main/gfx/screenshot1.png" width="40%"/> <img src="https://github.com/dkrajzew/tempo120/blob/main/gfx/screenshot3.png" width="40%"/>
<!-- imgs end -->

You may download an executable from the [releases page](https://github.com/dkrajzew/tempo120/releases). The latest version is 1.8.0.

# About

__Tempo120__ is a very simple car racing game. You may control your vehicle using the cursor keys or WASD.

The higher the speed the more difficult it is to control the vehicle. You do not need to accelerate all the time. The speed stays same unless you brake or drive besides the road.


# How to...

## Install

The most recent compiled version can be found on the [releases page](https://github.com/dkrajzew/tempo120/releases). This repository includes the source code and assets needed to build / extend the game.

## Build own levels/tracks

The game stores its tracks in .png-images. In theory, the images may have an arbitrary size, but you may encounter memory issues if they get too big.

Each pixel in the image represents a field within the game.

The track's background should be in (100, 255, 0, 255) green what is interpreted as grass. The track itself should be drawn on it using grey. I used (139, 139, 139, 255) as color and a plain, round brush with a size of 14 pixels. The track is surrounded by "tires" (0, 0, 0, 255) which stop the vehicle completely. In the default track, tires are placed in a distance of 7 pixels around the track.

A plain white (255, 255, 255, 255) line indicates the end of the track - when reaching it, the round ends and you may insert your name which may occur in the high scores.

There is a single plain red (255, 0, 0, 255) pixel on the track which defines the vehicle's starting position.

__If you build your own levels, don't forget to share them!__

## Build a standalone executable

You can build an executable using

```pyinstaller --onefile tempo120.py```

If you have ```pyinstaller``` installed...

You must then copy the assets folders (gfx, muzak) and optionally the scores into the generated dist folder, rename it to "tempo120" and zip it.

The executable runs on the type of machines you have executed pyinstaller at.


# Possible extensions

The first version of the game was written on a single day during a game jam. That's why the current version has only a limited functionality - driving along a race track, trying not to get off the road.

Possible extensions could be:

* adding other field types (water, obstacles)
* adding other vehicle types
* introducing something to avoid cheating (you can basically drive backwards...)
* introducing more rounds
* adding further tracks
* some kind of an integration of further tracks
* multiplayer mode

I like the game and may port it to c++ once.

# Change Log

## v1.8.0 (28.07.2024)

* adding pygame to setup requirements
* better handling of leaving the game using ESCAPE
* cleaning
* image correction
* renamed main branch to main

## v1.4.0 (06.08.2023)

* Loads assets both, when installed from PyPI and from the zip.

## v1.0.0 (03.08.2023)

* adding missing assets to the Python release

## v0.8.0 (02.08.2023)

* included track debugging from [MapleMonarch](https://maplemonarch.itch.io/)
* added a setup script, you may now download the current release from [PyPi](https://pypi.org/project/degrotesque/)

## v0.6.0 (23.07.2023)

* added tires to disallow cheating
* patched the engine noise (repeating, volume in dependence to speed)
* some smaller improvements

# Notes

* I tried to use bitmap tiles instead of simply filled polygons - the game gets much slower. One would have to move to using openGL in this case...

# License

The game is licensed under the GPL 3.0.


