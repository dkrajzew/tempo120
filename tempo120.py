#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
# ===========================================================================
"""tempo120 - A party car racing game."""
# ===========================================================================
__author__     = "Daniel Krajzewicz"
__copyright__  = "Copyright 2023-2024, Daniel Krajzewicz"
__credits__    = ["Daniel Krajzewicz"]
__license__    = "GPL 3.0"
__version__    = "1.6.0"
__maintainer__ = "Daniel Krajzewicz"
__email__      = "daniel@krajzewicz.de"
__status__     = "Production"
# ===========================================================================
# - https://github.com/dkrajzew/tempo120
# - http://www.krajzewicz.de
# ===========================================================================


# --- imports ---------------------------------------------------------------
from random import random
import os
import sys
import math
import pygame
import pygame.gfxdraw
from pygame.locals import *


# --- constants -------------------------------------------------------------
SIZE = 32
VIEW_WIDTH = 40
VIEW_HEIGHT = 25
SCR_WIDTH = VIEW_WIDTH * SIZE
SCR_HEIGHT = VIEW_HEIGHT * SIZE

INTRO_TITLE = 0
INTRO_SCORES = 1
BEGIN = 2
GAME = 3
SET_SCORE = 4

TILE_TRACK = (139, 139, 139, 255)
TILE_GRASS = (100, 255, 0, 255)
TILE_GOAL = (255, 255, 255, 255)
TILE_START = (255, 0, 0, 255)
TILE_TIRES = (0, 0, 0, 255)

 

# --- helper methods --------------------------------------------------------
def rotatePoint(p, center, angle):
    s = math.sin(angle);
    c = math.cos(angle);
    p[0] -= center[0]
    p[1] -= center[1]
    xnew = p[0] * c - p[1] * s
    ynew = p[0] * s + p[1] * c
    return [xnew + center[0], ynew + center[1]]


def rotate(poly, center, angle):
    ret = []
    for p in poly:
        ret.append(rotatePoint(p, center, angle))
    return ret

def nice_time(t):
    # https://stackoverflow.com/questions/35989666/convert-milliseconds-to-hours-min-and-seconds-python
    millis = int(t)
    seconds = (millis/1000)%60
    seconds = int(seconds)
    minutes = (millis/(1000*60))%60
    minutes = int(minutes)
    hours = (millis/(1000*60*60))%24
    return "%02d:%02d:%02d.%03d" % (hours, minutes, seconds, millis)


# --- game classes ----------------------------------------------------------
class Scores:
    """
    A class that reads, writes, and processes the high score table.
    
    Each entry consists of the player's name with a maximum length of 16 characters and 
    the needed time to accmplish the track in milliseconds. Within the high scores file
    "scores.txt" each entry is stored in one line, using tab ('\t') to divide the name 
    and the time.
    
    The list may include up to 15 entries. The player's name may be up to 16 characters
    long.
    """
    
    def __init__(self, path):
        """Loads the scores using the load method."""
        self._path = path
        self.load()
        

    def load(self):
        """Loads the scores.
        
        Loads scores from "scores.txt", sorts them by the needed time and prunes
        them to the maximum length of 15 entries.
        """
        scores = []
        try:
            with open(os.path.join(self._path, "scores", "scores.txt")) as fd:
                for l in fd:
                    name, t = l.strip().split("\t")
                    scores.append([name, int(t)])
            scores.sort(key=lambda x: x[1])
        except: pass
        self._scores = scores[:15]
        
        
    def save(self):
        """Saves the scores into "scores.txt"
        """
        fd = open(os.path.join(self._path, "scores", "scores.txt"), "w")
        for s in self._scores:
            fd.write("%s\t%s\n" % (s[0], s[1]))    
        fd.close()


    def add(self, name, t):
        """Adds an entry to the scores
        
        The name is added and the scores are sorted by time and pruned to
        the maximum length of 15 entries.
        """
        scores = []
        scores.append([name, t])
        scores.extend(self._scores)
        scores.sort(key=lambda x: x[1])
        self._scores = scores[:15]
        self.save()


    def draw(self, surface, font):
        """Draws the scores onto the given surface
        """
        img = font.render("Scores", True, (255, 255, 255))
        surface.blit(img, ((SCR_WIDTH-img.get_width())/2, 40))
        for i,s in enumerate(self._scores):
            img = font.render(s[0], True, (255, 255, 255))
            surface.blit(img, (300, 100 + i*40))
            img = font.render(nice_time(s[1]), True, (255, 255, 255))
            surface.blit(img, (SCR_WIDTH-300-img.get_width(), 100 + i*40))



class Track:
    """
    A class that stores the track.
    """
    
    def __init__(self, image):
        """Initialises the track
        """
        self._height = image.get_height()
        self._width = image.get_width()
        self._start_positions = []
        self._image = image
        for y in range(0, self._height):
            for x in range(0, self._width):
                col = self._image.get_at((x, y))
                #print (col)
                if col==TILE_START:
                    self._start_positions.append((x, y))
                    self._image.set_at((x, y), TILE_TRACK)

    
    def get_next_starting_position(self):
        """Returns the next (and currently only) starting position.
        """
        pos = self._start_positions[-1]
        return (pos[0]*SIZE, pos[1]*SIZE)
        
        
    def get_floor(self, x, y):
        """Returns the type of the floow that is below the given position.
        """
        return self._image.get_at((int(x/SIZE), int(y/SIZE)))
    
    
    def draw(self, surface, view):
        """Draws the track
        
        Well, ok. Computing the offset / initial (top left-most one) tile took me
        to long. I suppose there is a better way to do this.
        """
        # compute offsets
        xib = int(view.left/SIZE)
        yib = int(view.top/SIZE)
        xpb = -view.left % SIZE
        ypb = -view.top % SIZE
        if view.left<=0:
            xib -= 1
            xpb -= SIZE
        elif xpb!=0:
            xpb -= SIZE
        if view.top<=0:
            yib -= 1
            ypb -= SIZE
        elif ypb!=0:
            ypb -= SIZE
        # go through the tiles, draw each as a filled rectangle
        for yi,y in enumerate(range(yib, yib+VIEW_HEIGHT+1)):
            if y<0 or y>=self._height: continue
            for xi,x in enumerate(range(xib, xib+VIEW_WIDTH+1)):
                if x<0 or x>=self._width: continue
                yp = yi * SIZE + ypb
                xp = xi * SIZE + xpb
                p = []
                p.append([xp, yp])
                p.append([xp+SIZE, yp])
                p.append([xp+SIZE, yp+SIZE])
                p.append([xp, yp+SIZE])
                p.append([xp, yp])
                pygame.gfxdraw.filled_polygon(surface, p, self._image.get_at((x, y)))




class Vehicle:
    """A vehicle
    
    A vehicle mainly consists of a position, an orientation and an image.
    It has a velocity and a delta-orientation as well...
    """
    
    def __init__(self, x, y, o, image):
        """Initialises the vehicle"""
        self._x = x
        self._y = y
        self._o = o
        self._v = 0
        self._do = 0
        self._image = image
        self._offtrack = 0
        

    def draw(self, surface):
        """Draws the vehicle onto the given surface"""
        rot_image = pygame.transform.rotate(self._image, self._o)
        rot_rect = rot_image.get_rect(center=(8, 16))  
        rot_rect = rot_rect.move((SCR_WIDTH/2, SCR_HEIGHT/2))
        surface.blit(rot_image, rot_rect)


    def accel(self, dt, value):
        """Accelerates/decelerates the vehicle"""
        self._v = min(100, max(-10, self._v + value * dt))


    def steer(self, dt, value):
        """Steers the vehicle"""
        self._do += self._v * value


    def step(self, game, dt):
        """Performs a simulation step"""
        floor = game._track.get_floor(self._x, self._y)
        if floor==TILE_GOAL:
            game.track_finished()
            self._v = 0
            self._do = 0
        elif floor==TILE_GRASS:
            v = self._v
            if self._v>1:
                self.accel(dt, -10)
            else:
                self._v = max(-0.1, min(0.1, self._v))
            self._offtrack += dt
        elif floor==TILE_TIRES:
            self._v = 0
        self._o += self._do * dt
        while self._o>360:
            self._o -= 360
        while self._o<-360:
            self._o += 360
        ndo = max(0, abs(self._do)*.9)
        self._do = ndo if self._do>=0 else -ndo
        self._x += math.sin(self._o / 180 * math.pi) * self._v
        self._y += math.cos(self._o / 180 * math.pi) * self._v
        game._engine_sound.set_volume(max(.2, .2+.8*min(150, self._v*20)/150.))




class Ego(Vehicle):
    """The ego vehicle, just a derivation of Vehicle with no additional functionality"""
    
    def __init__(self, x, y, o, image):
        """Initialises the vehicle"""
        Vehicle.__init__(self, x, y, o, image)




class NPC(Vehicle):
    """An NPC vehicle, currently not used, just a derivation of Vehicle with no additional functionality"""
    def __init__(self, x, y, o, image):
        """Initialises the vehicle"""
        Vehicle.__init__(self, x, y, o, image)

    def step(self, game, dt):
        """Performs a simulation step"""
        Vehicle.step(self, x, y, o, image)



class Game:
    """The game class"""
    
    def __init__(self):
        """Initialises the game
        """
        path = os.path.dirname(__file__)
        if not os.path.exists(os.path.join(path, "gfx", "car.png")):
            path = "."
        self._car_image = pygame.image.load(os.path.join(path, "gfx", "car.png"))
        self._title_image = pygame.image.load(os.path.join(path, "gfx", "title.png"))
        track_image = pygame.image.load(os.path.join(path, "gfx", "track01.png"))
        self._theme_sound = pygame.mixer.Sound(os.path.join(path, "muzak", "track.ogg"))
        self._theme_sound.set_volume(1)
        self._engine_sound = pygame.mixer.Sound(os.path.join(path, "muzak", "engine.ogg"))
        self._engine_sound.set_volume(.2)
        self._font = pygame.font.SysFont(None, 48)
        self._height = track_image.get_height()
        self._width = track_image.get_width()
        self._track = Track(track_image)
        self._theme_channel = pygame.mixer.Channel(0)
        self._engine_channel = pygame.mixer.Channel(1)
        self._scores = Scores(path)
        self._start_time = 0
        self._last_entered_time = 0
        self._quit = False
        self._pressed_keys = set()
        self.init()
        

    def init(self):
        """Initialises a game run
        """
        start_position = self._track.get_next_starting_position()
        self._ego = Ego(start_position[0], start_position[1], 180, self._car_image)
        self._state = INTRO_TITLE
        self._theme_channel.play(self._theme_sound, loops=-1)    
        self._start_time = pygame.time.get_ticks()
        self._engine_channel.stop()    


    def draw(self, surface):
        """Performs the drawing (all screens)
        """
        surface.fill((0, 0, 0))
        xs = SCR_WIDTH/2
        ys = SCR_HEIGHT/2
        view = Rect(-xs+self._ego._x, -ys+self._ego._y, xs+xs, ys+ys)
        self._track.draw(surface, view)
        if self._state==INTRO_TITLE:
            blend_image = pygame.Surface((SCR_WIDTH, SCR_HEIGHT), pygame.SRCALPHA)
            pygame.draw.rect(blend_image, (0, 0, 0, 100), blend_image.get_rect())
            surface.blit(blend_image, (0, 0))
            surface.blit(self._title_image, (0, 0))
            dt = int((pygame.time.get_ticks() - self._start_time) / 1000)
            if dt>5:
                self._state = INTRO_SCORES
                self._start_time = pygame.time.get_ticks()
        elif self._state==INTRO_SCORES:
            blend_image = pygame.Surface((SCR_WIDTH, SCR_HEIGHT), pygame.SRCALPHA)
            pygame.draw.rect(blend_image, (0, 0, 0, 100), blend_image.get_rect())
            surface.blit(blend_image, (0, 0))
            self._scores.draw(surface, self._font)
            dt = int((pygame.time.get_ticks() - self._start_time) / 1000)
            if dt>5:
                self._state = INTRO_TITLE
                self._start_time = pygame.time.get_ticks()
        elif self._state==BEGIN:
            dt = int((pygame.time.get_ticks() - self._start_time) / 1000)
            img = self._font.render("%s" % (3-dt), True, (255, 255, 255))
            surface.blit(img, ((SCR_WIDTH-img.get_width())/2, 320))
            self._ego.draw(surface)
        elif self._state==GAME:
            self._ego.draw(surface)
            img = self._font.render("{:10.2f} km/h".format(self._ego._v*20), True, (255, 255, 255))
            surface.blit(img, (20, 20))
            level_time = pygame.time.get_ticks() - self._start_time
            img = self._font.render(nice_time(level_time), True, (255, 255, 255))
            surface.blit(img, (SCR_WIDTH-60-img.get_width(), 20))
        elif self._state==SET_SCORE:
            blend_image = pygame.Surface((SCR_WIDTH, SCR_HEIGHT), pygame.SRCALPHA)
            pygame.draw.rect(blend_image, (0, 0, 0, 100), blend_image.get_rect())
            surface.blit(blend_image, (0, 0))
            self._ego.draw(surface)
            img = self._font.render("Your time: " + nice_time(self._level_time), True, (255, 255, 255))
            surface.blit(img, ((SCR_WIDTH-img.get_width())/2, 320))
            img = self._font.render("Please enter your name:", True, (255, 255, 255))
            surface.blit(img, ((SCR_WIDTH-img.get_width())/2, 380))
            img = self._font.render(self._current_name, True, (255, 255, 255))
            surface.blit(img, ((SCR_WIDTH-img.get_width())/2, 440))
            

    def process_keys(self, dt):
        """Processes the key inputs
        """
        if self._state==INTRO_TITLE or self._state==INTRO_SCORES:
            if pygame.K_SPACE in self._pressed_keys:
                self._state = BEGIN
                self._start_time = pygame.time.get_ticks()
                self._theme_channel.stop()    
                self._engine_channel.play(self._engine_sound, loops=-1)    
            elif pygame.K_ESCAPE in self._pressed_keys:
                self._quit = True
        elif self._state==BEGIN:
            dt = int((pygame.time.get_ticks() - self._start_time) / 1000)
            if dt>2:
                self._state = GAME
                self._start_time = pygame.time.get_ticks()    
        elif self._state==GAME:
            k_left = pygame.K_LEFT in self._pressed_keys or pygame.K_a in self._pressed_keys
            k_right = pygame.K_RIGHT in self._pressed_keys or pygame.K_d in self._pressed_keys
            k_up = pygame.K_UP in self._pressed_keys or pygame.K_w in self._pressed_keys
            k_down = pygame.K_DOWN in self._pressed_keys or pygame.K_s in self._pressed_keys
            if k_left and not k_right:
                self._ego.steer(dt, 5)
            if k_right and not k_left:
                self._ego.steer(dt, -5)
            if k_up and not k_down:
                self._ego.accel(dt, 1)
            if k_down and not k_up:
                self._ego.accel(dt, -1)
            if pygame.K_ESCAPE in self._pressed_keys:
                self._state = INTRO_TITLE
                self._pressed_keys.remove(pygame.K_ESCAPE)
                self.init()


    def track_finished(self):
        """Closes the gaming mode, moves to user name entry
        """
        if self._state==SET_SCORE:
            return 
        self._current_name = ""
        self._pressed_keys = set()
        self._state = SET_SCORE
        self._level_time = pygame.time.get_ticks() - self._start_time
        self._start_time = pygame.time.get_ticks()
                

# --- main function ---------------------------------------------------------
def main(args=None):
    pygame.init()
    pygame.mixer.init()
    game = Game()
    surface = pygame.display.set_mode((SCR_WIDTH, SCR_HEIGHT))
    surface.fill((0, 0, 0))
    pygame.display.set_caption("Tempo120")

    t1 = pygame.time.get_ticks()
    while not game._quit:
        t2 = pygame.time.get_ticks()
        dt = (t2 - t1) / 1000.
        for event in pygame.event.get():              
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
            if event.type==pygame.KEYDOWN:
                game._pressed_keys.add(event.key)
                if game._state==SET_SCORE:
                    if event.key==pygame.K_BACKSPACE:
                        game._current_name = game._current_name[:-1]
                    elif event.key==pygame.K_RETURN:
                        game._scores.add(game._current_name, game._level_time)
                        game.init()
                    else:
                        game._current_name += event.unicode
                        if len(game._current_name)>16: game._current_name = game._current_name[:16]
            if event.type==pygame.KEYUP and event.key in game._pressed_keys:
                game._pressed_keys.remove(event.key)
        game.process_keys(dt)
        game._ego.step(game, dt)
        game.draw(surface)
        pygame.display.update()
        t1 = t2
    pygame.mixer.quit()


# -- main check
if __name__ == '__main__':
    main(sys.argv) # pragma: no cover
