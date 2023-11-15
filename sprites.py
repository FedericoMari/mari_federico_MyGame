# import all libraries, including settings 
import pygame as pg
from pygame.sprite import Sprite
from random import randint
from pygame.math import Vector2 as vec
import os
from math import floor
from random import *
from settings import *

# setup asset folders here - images sounds etc.
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'images')

# create a class for cooldown
class Cooldown():
    # sets all properties to zero when instantiated... (start time, event times for all new objects etc...)
    def __init__(self):
        self.current_time = 0
        self.event_time = 0
        self.delta = 0
        # ticking ensures the timer is counting...
    # must use ticking to count up or down
    def ticking(self):
        # using pg, time module is built-in within pg
        self.current_time = floor((pg.time.get_ticks())/1000)
        self.delta = self.current_time - self.event_time
    # resets event time to zero - resets w/ cd
    def event_reset(self):
        self.event_time = floor((pg.time.get_ticks())/1000)
    # sets current time, will come out as an int (chose not to display on screen)
    def timer(self):
        self.current_time = floor((pg.time.get_ticks())/1000)

# create a class for the player sprite
class Player(Sprite):
    # initialize the class, create obj that will later be instantiated
    def __init__(self, game):
        Sprite.__init__(self)
        # instantiate game to use for collisions defined in Sprites
        self.game = game
        # image asset is loaded into pygame, folder name first, and image or file name after
        self.image = pg.image.load(os.path.join(img_folder, 'theBell.png')).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (0, 0)
        self.pos = vec(WIDTH/2, HEIGHT/2)
        self.vel = vec(0,0)
        self.acc = vec(0,0) 
        # define player health, will decrease over time from mobs
        self.health = 100
        # instantiate the cd
        self.cd = Cooldown()

    # create sub-class for controls, pygame responds when each key is pressed
    def controls(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            # left three
            self.acc.x = -3
        if keys[pg.K_d]:
            # right three
            self.acc.x = 3
            # define jump in sub-class below, jump based on PLAYER_JUMP in settings
        if keys[pg.K_SPACE]:
            self.jump()
    
    # create child class for jump, depending on ground or plat, create separate collisions
    def jump(self):
        # differentiate jumps for ground and normal plat
        hits = pg.sprite.spritecollide(self, self.game.all_platforms, False)
        ghits = pg.sprite.collide_rect(self, self.game.ground)
        # plat
        if hits:
            if self.rect.y < hits[0].rect.y:
                print("i can jump")
                self.acc.y = -PLAYER_JUMP
        # ground, not really applicable as my game is a scroller
        if ghits:
            if self.rect.y < self.game.ground.rect.y:
                print("i can jump")
                self.acc.y = -PLAYER_JUMP
    def update(self):
        self.cd.ticking()
        # this prevents players from moving through the left side of the platforms...
        phits = pg.sprite.spritecollide(self, self.game.all_platforms, False)
        if self.vel[0] >= 0 and phits:
            if self.rect.right < phits[0].rect.left + 30:
                print("i just hit the left side of a box...")
                self.vel[0] = -self.vel[0]
                self.pos.x = phits[0].rect.left - 30
        # instantiate acceleration as a vector
        self.acc = vec(0,PLAYER_GRAV)
        self.controls()
        # if friction - apply here
        self.acc.x += self.vel.x * -PLAYER_FRIC
        # equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.rect.midbottom = self.pos
        # checks for mob hits
        # if you want to kill the mob when you collide change last argument to True
        mhits = pg.sprite.spritecollide(self, self.game.all_mobs, True)
        chits = pg.sprite.spritecollide(self, self.game.all_coins, True)
        
        # define both ghits and chits in sprites, if false it will disappear
        if chits:
            chits[0].tagged = False
            chits[0].cd.event_reset()
            chits[0].image.set_colorkey(WHITE)
        # if mob hits sets tagged to true 
        if mhits:
            mhits[0].tagged = False
            mhits[0].cd.event_reset()
            mhits[0].image = pg.image.load(os.path.join(img_folder, "explode.png")).convert()
            mhits[0].image.set_colorkey(BLACK)

# platform class, create different kinds of plats (moving or static)
class Platform(Sprite):
    def __init__(self, x, y, w, h, kind):
        Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(PURPLE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.kind = kind
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        # set speed to zero, will fluctuate depending on plat kind
        self.speed = 0
        if self.kind == "moving":
            self.speed = randint(0, 5)

    # update child clas, if plat is moving, set speed to self.rect.x
    def update(self):
        if self.kind == "moving":
            self.rect.x += self.speed
            if self.rect.x + self.rect.w > WIDTH-35 or self.rect.x - self.rect.w *0.5  < 0:
                self.speed = -self.speed
            elif self.rect.y + self.rect.h > HEIGHT/2 or self.rect.y < 0:
                self.speed = -self.speed

# create a mob class, assign game attribute from Game class
class Mob (Sprite):
    def __init__(self, game, x, y, w, h, kind):
        Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(BLACK)
        self.image = pg.image.load(os.path.join(img_folder, "image-15x15.jpg")).convert()
        self.game = game
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.kind = kind
        self.cd = Cooldown()
        self.pos = vec(WIDTH/2, HEIGHT/2)
        # set range of attack to 550, will start chasing with seeking func from far away
        self.hostile_range = 250
        self.tagged = False
        # creat bool value for seeking func, instantiate seeking 
        self.is_seeking = True
    
    # seeking child class (seeks based on limiting range defined in __init__ class)
    def seeking(self, obj):
        if abs(self.rect.x - obj.rect.x) < self.hostile_range and abs(self.rect.y - obj.rect.y) < self.hostile_range:
            if self.rect.x < obj.rect.x:
                self.rect.x += 1
            if self.rect.x > obj.rect.x:
                self.rect.x -= 1
            if self.rect.y < obj.rect.y:
                self.rect.y += 1
            if self.rect.y > obj.rect.y:
                self.rect.y -= 1
    
    # update child class for mobs
    def update(self):
        if self.is_seeking:
            self.seeking(self.game.player)
            self.cd.ticking()
        
        # delta time in cd tick
        if self.cd.delta > 0.4 and self.tagged:
            self.kill()

# couldn't get to figure this out...(final??)

# class for powers that will grant players increased jump or speed
# class Powers(Sprite):
#     def __init__(self, x, y, w, h, species):
#         Sprite.__init__(self)
#         self.image = pg.Surface((w, h))
#         self.image.fill(BLUE)
#         self.rect = self.image.get_rect()
#         self.rect.x = x
#         self.rect.y = y
#         self.species = species
#         self.speed = 0
#         if self.species == "jump boost":
#             self.speed = PLAYER_FRIC/2
#     def update(self):
#         pass
    

# class for Coins that will grant player powers or boosts, need to be addressed seriously
class Coins(Sprite):
    def __init__(self, x, y, w, h, kind):
        Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(WHITE)
        self.image = pg.image.load(os.path.join(img_folder, "image-15x15 (2).jpg")).convert()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.kind = kind
        self.pos = vec(WIDTH/2, HEIGHT/2)
        self.cd = Cooldown()
        self.tagged = True
    # update sub class, not necessary for now, so use pass to avoid errors
    def update(self):
        pass