# Tempo120

A racing game written using Python/pygame during the bpb (Bundeszentrale für politische Bildung) game jam 2023. The game jam's topic was mobility.

You may download an executable version on itch.io.

# About

_Tempo120_ is a very simple car racing game. You may control your vehicle using the cursor keys or WASD.

The higher the speed the more difficult is it to control the vehicle. You do not need to accelerate all the time. The speed stays same unless you brake or drive besides the road.

# Install

The most recent compiled version can be found on itch.io. This repository includes the source code and assets needed to build / extend the game.

# How to extend

## Levels/Tracks

The game stores its tracks in .png-images. In theory, the images may have an arbitrary size, but you may encounter memory issues if they get too big.

Each pixel in the image represents a field within the game. The most top left pixel must have the same color as the racing track.

The track's background should be in (100, 255, 0, 255) green what is interpreted as grass. The track itself should be drawn on it using grey. I used (139, 139, 139, 255) as color and a plain, round brush with a size of 14 pixels.

A plain white (255, 255, 255, 255) line indicates the end of the track - when reaching it, the round ends and you may insert your name which may occure in the high scores.

There is a single plain red (255, 0, 0, 255) pixel on the track which defines the vehicle's starting position.

_If you build your own levels, don't forget to share them!_

## Code of Conduct

!!!


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

