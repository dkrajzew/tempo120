# Tempo120

A racing game written using Python/pygame during the [bpb](https://www.bpb.de/) ([Bundeszentrale für politische Bildung](https://www.bpb.de/)) [game jam 2023](https://www.bpb.de/veranstaltungen/veranstaltungskalender/518950/bpb-game-jam-2023/). The game jam's topic was mobility.

You may download an executable version on [itch.io](https://dkrajzew.itch.io/tempo120).

# About

__Tempo120__ is a very simple car racing game. You may control your vehicle using the cursor keys or WASD.

The higher the speed the more difficult is it to control the vehicle. You do not need to accelerate all the time. The speed stays same unless you brake or drive besides the road.


# How to...

## Install

The most recent compiled version can be found on [itch.io](https://dkrajzew.itch.io/tempo120). This repository includes the source code and assets needed to build / extend the game.

## Build own Levels/Tracks

The game stores its tracks in .png-images. In theory, the images may have an arbitrary size, but you may encounter memory issues if they get too big.

Each pixel in the image represents a field within the game. The most top left pixel must have the same color as the racing track.

The track's background should be in (100, 255, 0, 255) green what is interpreted as grass. The track itself should be drawn on it using grey. I used (139, 139, 139, 255) as color and a plain, round brush with a size of 14 pixels.

A plain white (255, 255, 255, 255) line indicates the end of the track - when reaching it, the round ends and you may insert your name which may occure in the high scores.

There is a single plain red (255, 0, 0, 255) pixel on the track which defines the vehicle's starting position.

__If you build your own levels, don't forget to share them!__

## Build a standalone executable

You can build an executable using

```pyinstaller --onefile tempo120.py```

If you have ```pyinstaller``` installed...

You must then copy the assets folders (gfx, muzak) and optionally the scores into the generated dist folder.

The executable runs on the type of machines you have executed pyinstaller at.


# Possible extensions

The first version of the game was written on a single day during a game jam. That's why the current version has only a limited functionality - driving along a race track, trying not to get off the road.

Possible extensions could be:

* adding other field types (water, obstacles)
* adding other vehicle types
* introducing something to avoid cheating (you can basically drive backwards...)
* introducing more rounds
* some kind of an integration of further tracks
* multiplayer mode

I like the game and may port it to c++ once.


# License

The game is licensed under the GPL 3.0.


