from random import random
import os
import sys
import math
import pygame
import pygame.gfxdraw
from pygame.locals import *

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


class Scores:
    
    def __init__(self):
        self.load()
        

    def load(self):
        scores = []
        try:
            with open("scores.txt") as fd:
                for l in fd:
                    name, t = l.strip().split("\t")
                    scores.append([name, int(t)])
            scores.sort(key=lambda x: x[1])
        except: pass
        self._scores = scores[:15]
        
        
    def save(self):
        fd = open("scores.txt", "w")
        for s in self._scores:
            fd.write("%s\t%s\n" % (s[0], s[1]))    
        fd.close()


    def add(self, name, t):
        scores = []
        scores.append([name, t])
        scores.extend(self._scores)
        scores.sort(key=lambda x: x[1])
        self._scores = scores[:15]
        self.save()


    def draw(self, surface):
        img = font.render("Scores", True, (255, 255, 255))
        surface.blit(img, ((SCR_WIDTH-img.get_width())/2, 40))
        for i,s in enumerate(self._scores):
            img = font.render(s[0], True, (255, 255, 255))
            surface.blit(img, (300, 100 + i*40))
            img = font.render(nice_time(s[1]), True, (255, 255, 255))
            surface.blit(img, (SCR_WIDTH-300-img.get_width(), 100 + i*40))



class Track:
    def __init__(self, image):
        self._height = image.get_height()
        self._width = image.get_width()
        self._start_positions = []
        self._matrix = []
        green = image.get_at((0, 0))
        for y in range(0, self._height):
            line = []
            for x in range(0, self._width):
                col = image.get_at((x, y))
                if col==(255, 0, 0, 255):
                    self._start_positions.append((x, y))
                    col = green
                line.append(col)
            self._matrix.append(line)

    
    def get_next_starting_position(self):
        pos = self._start_positions[-1]
        return (pos[0]*SIZE, pos[1]*SIZE)
        
        
    def get_floor(self, x, y):
        return self._matrix[int(y/SIZE)][int(x/SIZE)]
    
    
    def draw(self, surface, view):
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
                if self._matrix[y][x]==None: continue
                yp = yi * SIZE + ypb
                xp = xi * SIZE + xpb
                p = []
                p.append([xp, yp])
                p.append([xp+SIZE, yp])
                p.append([xp+SIZE, yp+SIZE])
                p.append([xp, yp+SIZE])
                p.append([xp, yp])
                pygame.gfxdraw.filled_polygon(surface, p, self._matrix[y][x])




class Vehicle:
    
    def __init__(self, x, y, o, image):
        self._x = x
        self._y = y
        self._o = o
        self._v = 0
        self._do = 0
        self._image = image
        self._offtrack = 0
        

    def draw(self, surface):
        rot_image = pygame.transform.rotate(self._image, self._o)
        rot_rect = rot_image.get_rect(center=(8, 16))  
        rot_rect = rot_rect.move((SCR_WIDTH/2, SCR_HEIGHT/2))
        surface.blit(rot_image, rot_rect)


    def accel(self, dt, value):
        self._v = min(100, max(-10, self._v + value * dt))


    def steer(self, dt, value):
        self._do += self._v * value


    def step(self, game, dt):
        floor = game._track.get_floor(self._x, self._y)
        if floor==(255, 255, 255, 255):
            game.track_finished()
            self._v = 0
            self._do = 0
        elif floor==(100, 255, 0, 255):
            v = self._v
            if self._v>1:
                self.accel(dt, -10)
            else:
                self._v = max(-0.1, min(0.1, self._v))
            self._offtrack += dt
        self._o += self._do * dt
        while self._o>360:
            self._o -= 360
        while self._o<-360:
            self._o += 360
        ndo = max(0, abs(self._do)*.9)
        self._do = ndo if self._do>=0 else -ndo
        self._x += math.sin(self._o / 180 * math.pi) * self._v
        self._y += math.cos(self._o / 180 * math.pi) * self._v




class Ego(Vehicle):
    
    def __init__(self, x, y, o, image):
        Vehicle.__init__(self, x, y, o, image)




class NPC(Vehicle):
    def __init__(self, x, y, o, image):
        Vehicle.__init__(self, x, y, o, image)

    def step(self, game, dt):
        Vehicle.step(self, x, y, o, image)



class Game:
    def __init__(self, image, car):
        self._height = image.get_height()
        self._width = image.get_width()
        self._track = Track(image)
        self._scores = Scores()
        self._start_time = 0
        self._last_entered_time = 0
        self.init()

    def init(self):
        start_position = self._track.get_next_starting_position()
        self._ego = Ego(start_position[0], start_position[1], 180, car)
        self._state = INTRO_TITLE
        theme_channel.play(theme_sound)    
        self._start_time = pygame.time.get_ticks()
        engine_channel.stop()    

    def draw(self, surface):
        surface.fill((0, 0, 0))
        xs = SCR_WIDTH/2
        ys = SCR_HEIGHT/2
        view = Rect(-xs+self._ego._x, -ys+self._ego._y, xs+xs, ys+ys)
        self._track.draw(surface, view)
        if self._state==INTRO_TITLE:
            blend_image = pygame.Surface((SCR_WIDTH, SCR_HEIGHT), pygame.SRCALPHA)
            pygame.draw.rect(blend_image, (0, 0, 0, 100), blend_image.get_rect())
            surface.blit(blend_image, (0, 0))
            surface.blit(title, (0, 0))
            dt = int((pygame.time.get_ticks() - self._start_time) / 1000)
            if dt>5:
                self._state = INTRO_SCORES
                self._start_time = pygame.time.get_ticks()
        elif self._state==INTRO_SCORES:
            blend_image = pygame.Surface((SCR_WIDTH, SCR_HEIGHT), pygame.SRCALPHA)
            pygame.draw.rect(blend_image, (0, 0, 0, 100), blend_image.get_rect())
            surface.blit(blend_image, (0, 0))
            self._scores.draw(surface)
            dt = int((pygame.time.get_ticks() - self._start_time) / 1000)
            if dt>5:
                self._state = INTRO_TITLE
                self._start_time = pygame.time.get_ticks()
        elif self._state==BEGIN:
            dt = int((pygame.time.get_ticks() - self._start_time) / 1000)
            img = font.render("%s" % (3-dt), True, (255, 255, 255))
            surface.blit(img, ((SCR_WIDTH-img.get_width())/2, 320))
            self._ego.draw(surface)
        elif self._state==GAME:
            self._ego.draw(surface)
            img = font.render("{:10.2f} km/h".format(game._ego._v*20), True, (255, 255, 255))
            surface.blit(img, (20, 20))
            level_time = pygame.time.get_ticks() - self._start_time
            img = font.render(nice_time(level_time), True, (255, 255, 255))
            surface.blit(img, (SCR_WIDTH-60-img.get_width(), 20))
        elif self._state==SET_SCORE:
            blend_image = pygame.Surface((SCR_WIDTH, SCR_HEIGHT), pygame.SRCALPHA)
            pygame.draw.rect(blend_image, (0, 0, 0, 100), blend_image.get_rect())
            surface.blit(blend_image, (0, 0))
            self._ego.draw(surface)
            img = font.render("Your time: " + nice_time(self._level_time), True, (255, 255, 255))
            surface.blit(img, ((SCR_WIDTH-img.get_width())/2, 320))
            img = font.render("Please enter your name:", True, (255, 255, 255))
            surface.blit(img, ((SCR_WIDTH-img.get_width())/2, 380))
            img = font.render(self._current_name, True, (255, 255, 255))
            surface.blit(img, ((SCR_WIDTH-img.get_width())/2, 440))

    def process_keys(self, dt):
        if self._state==INTRO_TITLE or self._state==INTRO_SCORES:
            if pygame.K_SPACE in pressed_keys:
                self._state = BEGIN
                self._start_time = pygame.time.get_ticks()
                theme_channel.stop()    
                engine_channel.play(engine_sound)    
        elif self._state==BEGIN:
            dt = int((pygame.time.get_ticks() - self._start_time) / 1000)
            if dt>2:
                self._state = GAME
                self._start_time = pygame.time.get_ticks()    
        elif self._state==GAME:
            k_left = pygame.K_LEFT in pressed_keys or pygame.K_a in pressed_keys
            k_right = pygame.K_RIGHT in pressed_keys or pygame.K_d in pressed_keys
            k_up = pygame.K_UP in pressed_keys or pygame.K_w in pressed_keys
            k_down = pygame.K_DOWN in pressed_keys or pygame.K_s in pressed_keys
            if k_left and not k_right:
                self._ego.steer(dt, 5)
            if k_right and not k_left:
                self._ego.steer(dt, -5)
            if k_up and not k_down:
                self._ego.accel(dt, 1)
            if k_down and not k_up:
                self._ego.accel(dt, -1)
            if pygame.K_ESCAPE in pressed_keys:
                self._state = INTRO_TITLE
                self.init()

    def track_finished(self):
        if self._state==SET_SCORE:
            return 
        self._current_name = ""
        pressed_keys = set()
        self._state = SET_SCORE
        self._level_time = pygame.time.get_ticks() - self._start_time
        self._start_time = pygame.time.get_ticks()
                

pygame.init()
pygame.mixer.init()
theme_channel = pygame.mixer.Channel(0)
engine_channel = pygame.mixer.Channel(1)
car = pygame.image.load("./gfx/car.png")
title = pygame.image.load("./gfx/title.png")
image = pygame.image.load("./gfx/track01.png")
theme_sound = pygame.mixer.Sound("racing-track.ogg")
theme_sound.set_volume(1)
engine_sound = pygame.mixer.Sound("race-car-engine.ogg")
engine_sound.set_volume(1)
game = Game(image, car)
surface = pygame.display.set_mode((SCR_WIDTH, SCR_HEIGHT))
surface.fill((0, 0, 0))
pygame.display.set_caption("Tempo 120")
font = pygame.font.SysFont(None, 48)

t1 = pygame.time.get_ticks()
pressed_keys = set()
while True:
    t2 = pygame.time.get_ticks()
    dt = (t2 - t1) / 1000.
    for event in pygame.event.get():              
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            pressed_keys.add(event.key)
            if game._state==SET_SCORE:
                if event.key==pygame.K_BACKSPACE:
                    game._current_name = game._current_name[:-1]
                elif event.key==pygame.K_RETURN:
                    game._scores.add(game._current_name, game._level_time)
                    game.init()
                else:
                    game._current_name += event.unicode
                    if len(game._current_name)>16: game._current_name = game._current_name[:16]
        if event.type == pygame.KEYUP:
            pressed_keys.remove(event.key)

    game.process_keys(dt)
    game._ego.step(game, dt)
    game.draw(surface)
    pygame.display.update()
    t1 = t2

pygame.mixer.quit()