# this file was created by Federico Mari on 10/9/2023
# import libraries and packages
# content from kids can code: http://kidscancode.org/blog/
# content from Cris Cozort 

# import libraries and modules
'''
Game Design: 
Rules: cannot pass through a platform without losing points, lose points when hitting mobs
Goals: collect coins to increase score, then avoid the mobs that have a seeking function, keep going up while playing game
Feedback: have been working on the coin class for days, still not functioning
Design: try to incorporate a backgroud for the fill, was able to 
Freedom: create plats that continue to spawn as one keeps on traveling to the right, continue to spawn as going up

Goals for code:
have a saved world where you can trace your steps back and move forwards between them, keep going up as if they were levels
'''
# import all libraries including settings and sprites
import pygame as pg
from pygame import * 
from pygame.sprite import Sprite
import random
from random import randint
import os
# not necessary, pg has Clock module (time)
import time
from settings import *
from sprites import *
# import vector, for plats, collisions, and movement
vec = pg.math.Vector2

# setup asset folders here - images sounds etc.
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'images')

# create game class, instantiate obj
class Game:
    def __init__(self):
        # init pygame and create a window
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("The Climb")
        self.clock = pg.time.Clock()
        self.running = True
        self.paused = False
        # establish a cooldown, defined in sprites
        self.cd = Cooldown()
    
    # create a class for new assets, all sprites for mobs, coins, etc...
    def new(self):
        # create a background image for the screen, given by C. Cozort
        self.bgimage = pg.image.load(os.path.join(img_folder, "image-720x700.jpg")).convert()
        # create a score, added to or subtracted depending on collisions
        self.score = 0
        # create a group for all sprites
        self.all_sprites = pg.sprite.Group()
        self.all_platforms = pg.sprite.Group()
        # self.all_powers = pg.sprite.Group()
        self.all_mobs = pg.sprite.Group()
        self.all_coins = pg.sprite.Group()
        # instantiate classes
        self.player = Player(self)
        # add instances to groups
        self.all_sprites.add(self.player)
        # self.powers = Powers(35, 60, 20, 20, "jump boost")
        self.ground = Platform(*GROUND)
        self.all_sprites.add(self.ground)
        # create different platforms within the defined args of list in settings 
        for p in PLATFORM_LIST:
            # instantiation of the Platform class
            plat = Platform(*p)
            self.all_sprites.add(plat)
            self.all_platforms.add(plat)
            # create different mobs from 0-40 of them on screen
        for m in range(0,40):
            m = Mob(self, randint(0, WIDTH), randint(0, HEIGHT/2), 15, 15, "normal")
            self.all_sprites.add(m)
            self.all_mobs.add(m)
        self.run()
        # create all coins to be collected, need to troubleshoot this, only works when you click the X
        for c in range(0,30):
            c = Coins(randint(0, WIDTH), randint(0, HEIGHT/2), 15, 15, "normal")
            self.all_sprites.add(c)
            self.all_coins.add(c)
        self.run()

    # func to establish the time ticks based on FPS (30) and if playing, continue updating sprites
    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            if not self.paused:
                self.update()
            # draw regardless, even if paused
            self.draw()

    def update(self):
        # define all sprites as being updated
        self.all_sprites.update()
        # cooldown runs w/ FPS
        self.cd.ticking()
        # define all collisions in the main
        mhits = pg.sprite.spritecollide(self.player, self.all_mobs, True)
        # collisions for mobs only
        if mhits:
            self.player.health -= 20
        self.all_sprites.update()
        if self.player.pos.x < 0:
            self.player.pos.x = WIDTH
        if self.player.pos.x > WIDTH: 
            self.player.pos.x = 0
        
        # move plats up in group as you reach a point on screen
        if self.player.pos.y < WIDTH:
            for p in self.all_platforms:
                p.rect.y += 0.75
                self.ground.rect.y += 0.75

        # this is what prevents the player from falling through the platform when falling down...
        hits = pg.sprite.spritecollide(self.player, self.all_platforms, False)
        # collisions for plats only in main
        if hits:
            if hits[0].kind == "moving":
                self.player.vel.x = hits[0].vel.x
            if self.player.vel.y > 0:
                self.player.pos.y = hits[0].rect.top 
                self.player.vel.y = 0
                # print(self.player.vel.y)
                # print(self.player.acc.y)
            elif self.player.vel.y < 0:
                self.player.vel.y = -self.player.vel.y/2
            
        # checks to see if player collides specifically with the ground and sets him on top of it
        ghits = pg.sprite.collide_rect(self.player, self.ground)
        # collisions for ground only, flat surface on the bottom of screen rect
        if ghits:
            self.player.pos.y = self.ground.rect.top
            self.player.vel.y = 0
            if self.player.cd.delta == 2:
                print(self.player.cd.delta)
                self.player.cd.event_reset()
                self.player.health -= 10
        chits = pg.sprite.spritecollide(self.player, self.all_coins, True)
        # collisions for coins only, must troubleshoot issue with them
        if chits:
            self.player.score += 10
        if self.player.pos.x < 0:
            self.player.pos.x = WIDTH
        if self.player.pos.x > WIDTH: 
            self.player.pos.x = 0

        # continue scrolling to the right (2 pixels at a time) for all plats
        if self.player.pos.x > WIDTH/1.75:
            for self.p in self.all_platforms:
                self.p.rect.x -= 1
                self    

        # this prevents the player from jumping up through a platform
        if self.player.vel.y < 0:
            hits = pg.sprite.spritecollide(self.player, self.all_platforms, False)
            ghits = pg.sprite.spritecollide(self.player, self.all_platforms, False)
            
            # for both ground collisions and plat collisions, take away points
            if hits or ghits:
                self.score -= 10
                # make sure player does not jump straight through the plats
                if self.player.rect.bottom >= hits[0].rect.top - 1:
                    self.player.rect.top = hits[0].rect.bottom
                    self.player.vel.y = 0
    def events(self):
        for event in pg.event.get():
        # check for closed window, if it satisfies quit game
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                    self.playing = self.player.pos.y < 100
                self.running = False
            if self.player.health <= 0:
                self.running = False
                pg.QUIT
        # # establish all keyclicks as events
        # keys = pg.key.get_pressed()
        # if keys [pg.K_p]:
        #     self.cd.event_reset()

    # define all sprites that can be created on display screen
    def draw(self):
        ############ Draw ################
        # draw the background screen
        self.screen.fill(BLUE)
        self.screen.blit(self.bgimage, (0,0))
        # draw all sprites
        self.all_sprites.draw(self.screen)
        self.draw_text("Score: " + str(self.score), 22, WHITE, WIDTH/2, HEIGHT/10)
        self.draw_text("Health: " + str(self.player.health), 22, WHITE, WIDTH/2, HEIGHT/24)
        # buffer - after drawing everything, flip display
        pg.display.flip()
    
    # func for the formatting or syntax of the sprites drawn
    def draw_text(self, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface, text_rect)

    # not necessary yet, maybe for final?
    def show_start_screen(self):
        pass
    def show_go_screen(self):
        pass


# game loop engine, while loop is true, will run the game infinitely unless "pg.quit"
g = Game()
while g.running:
    g.new() 
    pg.time.Clock()

pg.quit()