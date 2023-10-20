# this file was created by Federico Mari on 10/9/2023
# import libraries and packages
import pygame as pg
from pygame.sprite import Sprite
from random import *
import os
from settings import *


vec = pg.math.Vector2

# setup asset folders and join image/ game folder
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'images')

# player settings
PLAYER_JUMP = 30
PLAYER_GRAV = 1.5

# define the colors to be used for background/character
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GRAY = (128, 128, 128)
HOT_RED = (247, 52,43)
GREEN = (0,255,0)
BLUE = (0,0,255)

def draw_text(text, size, color, x, y):
    font_name = pg.font.match_font('arial')
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    screen.blit(text_surface, text_rect)

# class for player sprite, initialize with __init__ (must have an upper-case for class + Sprite, another convention)
# Sprite = Super class
class Player(Sprite):
    # self is a sub-class, still initialized with __init__
    def __init__(self):
        Sprite.__init__(self)
        # self.image = pg.Surface((50, 50))
        # self.image.fill(GREEN)
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
        hits = pg.sprite.spritecollide(self, all_platforms, False)
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
        if player.rect.x > self.rect.x:
            self.rect.x += 1
        elif player.rect.x < self.rect.x:
            self.rect.x -= 1
        elif player.rect.y > self.rect.y:
            self.rect.y += 1
        elif player.rect.y > self.rect.y:
            self.rect.y += 1
    def update(self):
        self.seeking()

# init pygame and create a window
pg.init()
pg.mixer.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Welcome to Hell...")
clock = pg.time.Clock()

# create a group for all sprites
all_sprites = pg.sprite.Group()
all_platforms = pg.sprite.Group()
all_mobs = pg.sprite.Group()

# instantiate the classes:
player = Player()

# add player to all Sprites
all_sprites.add(player) 

for p in PLATFORM_LIST:
    # class is like the DNA and instance is "baby"
    # instantiation of the plat using p in list 
    plat = Platform(*p)
    all_sprites.add(plat)
    all_platforms.add(plat)

for m in range(0,25):
    m = Mob(randint(0, WIDTH), randint(0, HEIGHT/2), 20, 20, "hostile")
    all_sprites.add(m)
    all_mobs.add(m)

# create loop with boolean
running = True
while running:  
    # keep the loop running w/ the clock
    clock.tick(FPS)
    for event in pg.event.get():
        # check for closed window:
        if event.type == pg.QUIT:
            running = False

    ######### Update ############
    # update all sprites
    all_sprites.update()

    # this is what prevents the player from falling through the platform when falling down...
    if player.vel.y > 0:
            hits = pg.sprite.spritecollide(player, all_platforms, False)
            if hits:
                player.pos.y = hits[0].rect.top
                player.vel.y = 0

     # this prevents the player from jumping up through a platform
    if player.vel.y < 0:
        hits = pg.sprite.spritecollide(player, all_platforms, True) # False?
        if hits:
            print("ouch")
            SCORE -= 1
            if player.rect.bottom >= hits[0].rect.top - 5:
                player.rect.top = hits[0].rect.bottom
                player.acc.y = 5
                player.vel.y = 0

    ############ Draw ############
    # draw the screen
    screen.fill(GRAY)
    draw_text("Score:" + str(SCORE), 22, WHITE, WIDTH/2, HEIGHT/10)
    draw_text("FPS:" + str(FPS), 22, WHITE, WIDTH/2, HEIGHT/10 + 30)
    # draw all sprites
    all_sprites.draw(screen)
    # buffer -- after drawing, flip the display
    pg.display.flip()

pg.quit()