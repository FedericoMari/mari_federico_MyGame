# this file was created by: Federico Mari

import pygame as pg 
import os
from settings import *
vec = pg.math.Vector2
from pygame.sprite import Sprite

# setup asset folders and join image/ game folder
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'images')

class Player(Sprite):
    # self is a sub-class, still initialized with __init__
    def __init__(self, game):
        Sprite.__init__(self)
        # self.image = pg.Surface((50, 50))
        # self.image.fill(GREEN)
        self.game = game
        self.image = pg.image.load(os.path.join(img_folder, 'theBell.png')).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.pos = vec(WIDTH/2, HEIGHT/2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        print(self.rect.center)
    def controls(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.acc.x = -5
        elif keys[pg.K_d]:
            self.acc.x = 5
        elif keys[pg.K_w]:
            self.acc.y = -5
        elif keys[pg.K_s]:
            self.acc.y = 5
        elif keys[pg.K_SPACE]:
            self.jump()
    def jump(self):
        hits = pg.sprite.spritecollide(self, self.game.all_platforms, False)
        if hits:
            print("I can jump")
            self.vel.y = -PLAYER_JUMP
    def update(self):
        # self.rect.x += 5
        # self.rect.y += 10
        player_friction = -0.19
        self.acc = vec(0, PLAYER_GRAV)
        self.controls()
        # if friction - apply here:
        self.acc.x += self.vel.x * player_friction
        self.acc.y += self.vel.y * player_friction
        # equations of motion 
        self.vel += self.acc
        # continue to add vel and half of the acc
        self.pos += self.vel + 0.5*self.acc
        self.rect.midbottom = self.pos

# platform sprite, how to know where collisions are
class Platform(Sprite):
    def __init__(self, x, y, w, h, kind):
        Sprite.__init__(self)
        self.image = pg.Surface((w,h))
        self.image.fill(HOT_RED)
        self.rect = self.image.get_rect()
        self.rect.x = x 
        self.rect.y = y 
        self.kind = kind
    def update(self):
        if self.kind == "moving":
            self.pos = self.rect.x 
            self.rect.x = self.pos + 2
            if self.pos == WIDTH:
                self.rect.x

# create a platform for another platform for ice plat, lower friction 
class Ice_plat(Platform):
    def __init__(self, x, y, w, h, kind):
        Platform.__init__(self, x, y, w, h, kind)
        self.image = pg.Surface((w,h))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x 
        self.rect.y = y
        print("There's an ice plat!")

class Mob(Sprite):
    def __init__(self,x,y,w,h,kind):
        Sprite.__init__(self)
        self.image = pg.image.load(os.path.join(img_folder, 'the_anti_bell.png')).convert()
        self.image.set_colorkey (BLACK and GRAY)
        WIDTH = w
        HEIGHT = h
        self.rect = self.image.get_rect()
        self.rect.center = (w/2, h/2)
        self.pos = vec(w/2, h/2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.x = x 
        self.rect.y = y
        self.kind = kind
        # self.image = pg.Surface((w,h))
        # self.image.fill(BLUE)
    def seeking(self):
        # placeholder, could be enchanced using machine learning or AI
        if self.player.rect.x > self.rect.x:
            self.rect.x += 1
        elif self.player.rect.x < self.rect.x:
            self.rect.x -= 1
        elif self.player.rect.y > self.rect.y:
            self.rect.y += 1
        elif self.player.rect.y > self.rect.y:
            self.rect.y += 1
    def update(self):
        self.seeking()