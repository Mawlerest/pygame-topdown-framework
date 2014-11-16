import pygame
import sys
import os
import random
from menu import *


class Player(pygame.sprite.Sprite):
    # constructor for this class
    def __init__(self):
        # call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join('images', 'baloon.png'))
	self.image=pygame.transform.smoothscale(self.image,(2*30,3*30))
        self.rect = self.image.get_rect()
	self.rect.x=0
	self.rect.y=0
        self.speed = [0, 0]
	self.jumps =3
	self.maxspeed=2
	self.distance=5

    def jump(self):
	if(self.jumps>0):
	    self.speed[1]-=16
	    self.jumps-=1

    def move(self):
        # move the rect by the displacement ("speed")
        self.rect = self.rect.move(self.speed)
	self.distance+=self.speed[0]


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x):
        pygame.sprite.Sprite.__init__(self)
        # load the PNG
        self.image = pygame.image.load(os.path.join('images', 'ball.png'))
        self.rect = self.image.get_rect()
        self.rect.topleft = random.randrange(x,x+200), random.randrange(0,340)

class Block(pygame.sprite.Sprite):
    def __init__(self,x,y,w,h):
        pygame.sprite.Sprite.__init__(self)
        # load the PNG
        # color the surface cyan
        self.image=image=pygame.image.load(os.path.join('images', 'Back.png'))
	self.image=image=pygame.transform.smoothscale(self.image,(610,400))
        self.rect = self.image.get_rect()
        self.rect.topleft = x,y

class Floor(pygame.sprite.Sprite):
    def __init__(self,x,y,w,h):
        pygame.sprite.Sprite.__init__(self)
        # load the PNG
        # color the surface cyan
        self.image=pygame.image.load(os.path.join('images', 'lava.png'))
	self.image=pygame.transform.smoothscale(self.image,(600,30))
        self.rect = self.image.get_rect()
        self.rect.topleft = x,y

def event_loop(state):
    # get the pygame screen and create some local vars
    screen = pygame.display.get_surface()
    screen_rect = screen.get_rect()
    screen_width = screen.get_width()
    screen_height = screen.get_height()
    # set up font
    basicFont = pygame.font.SysFont(None, 24)
    # initialize a clock
    clock = pygame.time.Clock()
    # initialize the score counter
    score = 0
    # initialize the enemy speed
    enemy_speed = [6, 6]
    dead=False
    
    # initialize the player and the enemy
    player = Player()
    player.rect.height=60
    floor1 = Floor(0, screen_height-28, screen_width, 20)
    floor2 = Floor(screen_width, screen_height-28, screen_width, 20)
    wall= Block(-screen_width-50, 0, 10, screen_height)
    pannel1=Block(0, 0, screen_width, screen_height)
    pannel2=Block(screen_width, 0, screen_width, screen_height)

    back_list = pygame.sprite.Group()
    back_list.add(pannel1)
    back_list.add(pannel2)

    floor_list=pygame.sprite.Group()
    floor_list.add(floor1)
    floor_list.add(floor2)
    
    # create a sprite group for enemies only to detect collisions
    enemy_list = pygame.sprite.Group()
    sprite_list = pygame.sprite.Group()
    for x in range(0, random.randrange(3,7)):
	enemy = Enemy(300)
	sprite_list.add(enemy)
	enemy_list.add(enemy)
	
    # create a sprite group for the player and enemy
    # so we can draw to the screen
    sprite_list.add(player)
    sprite_list.add(wall)

    # main game loop
    while not(dead):
        # handle input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.speed[0]-=4
                elif event.key == pygame.K_RIGHT:
                    player.speed[0]+=4
                elif event.key == pygame.K_UP:
                    player.jump()
		elif event.key == pygame.K_ESCAPE:
		    sys.exit()


            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    player.speed[0]+=4
                elif event.key == pygame.K_RIGHT:
                    player.speed[0]-=4
  

	if(player.speed[1]<player.maxspeed):
	    player.speed[1]+=1
        
        # call the move function for the player
        player.move()

        # check player bounds
        if player.rect.left < 0:
            player.rect.left = 0
        if player.rect.right > screen_width/3:
            player.rect.right = screen_width/3
	    pannel1.rect.x-=4
	    pannel2.rect.x-=4
	    RotateBack(back_list)
	    floor1.rect.x-=4
	    floor2.rect.x-=4
	    RotateFloor(floor_list)
	    MoveEnemies(enemy_list)
        if player.rect.top < 0:
            player.rect.top = 0
        if player.rect.bottom > screen_height:
            player.rect.bottom = screen_height

        # detect all collisions between the player and enemy
        # but don't remove enemy after collisions
        # increment score if there was a collision
        if pygame.sprite.spritecollide(player, enemy_list, True):
            player.jumps+=1
	pygame.sprite.spritecollide(wall, enemy_list, True)

	if(pygame.sprite.spritecollide(player, floor_list, False)):
		dead=True
	   
	if(player.distance%(max(400/player.maxspeed,50))<4):
		auxenemy=Enemy(screen_width)
		enemy_list.add(auxenemy)
		sprite_list.add(auxenemy)
		player.distance+=1

	player.maxspeed=(player.distance/1000)+2
		

        # black background
        screen.fill((0, 0, 0))

        back_list.draw(screen)
	floor_list.draw(screen)

        # draw the player and enemy sprites to the screen
        sprite_list.draw(screen)

        # set up the score text
        text = basicFont.render('Float: %d Distance: %d' % (player.jumps, player.distance), True, (255, 255, 255))
        textRect = text.get_rect()
        textRect.centerx = screen_rect.centerx
        textRect.y = 0

        # draw the text onto the surface
        screen.blit(text, textRect)

        # update the screen
        pygame.display.flip()

        # limit to 45 FPS
        clock.tick(45)

    while(dead):

	dead=False
	text = basicFont.render('Dead', True, (255, 255, 255))
        textRect = text.get_rect()
        textRect.centerx = screen_rect.centerx
        textRect.centery = screen_rect.centery
        
	screen.fill((0, 0, 0))

        # draw the text onto the surface
        screen.blit(text, textRect)

	pygame.display.flip()

def RotateBack(back_list):
	for x in back_list:
		if(x.rect.right<=0):
			x.rect.x=x.rect.width

def RotateFloor(floor_list):
	for x in floor_list:
		if(x.rect.right<=0):
			x.rect.x=x.rect.width

def MoveEnemies(enemies):
	for e in enemies:
		e.rect.x-=4
		
def ImageList(i):
	if(i==0):
	    image=pygame.image.load(os.path.join('images', 'lava.png'))
	    image=pygame.transform.smoothscale(self.image,(600,400))
	    return img

def main():
    # initialize pygame
    pygame.init()

    # create the window
    size = width, height = 600, 400
    screen = pygame.display.set_mode(size)

    # set the window title
    pygame.display.set_caption("Lead Baloon")

    # create the menu
    menu = cMenu(50, 50, 20, 5, 'vertical', 100, screen,
                 [('Start Game',   1, None),
                  ('Exit',         3, None)])
    # center the menu
    menu.set_center(True, True)
    menu.set_alignment('center', 'center')

    # state variables for the finite state machine menu
    state = 0
    prev_state = 1

    # ignore mouse and only update certain rects for efficiency
    pygame.event.set_blocked(pygame.MOUSEMOTION)
    rect_list = []

    while 1:
        # check if the state has changed, if it has, then post a user event to
        # the queue to force the menu to be shown at least once
        if prev_state != state:
            pygame.event.post(pygame.event.Event(EVENT_CHANGE_STATE, key = 0))
            prev_state = state

        # get the next event
        e = pygame.event.wait()

        # update the menu
        if e.type == pygame.KEYDOWN or e.type == EVENT_CHANGE_STATE:
            if state == 0:
                # "default" state
                rect_list, state = menu.update(e, state)
            elif state == 1:
                # start the game
                event_loop(state)
            elif state == 2:
                # just to demonstrate how to make other options
                pygame.display.set_caption("y u touch this")
                state = 0
            else:
                # exit the game and program
                pygame.quit()
                sys.exit()

            # quit if the user closes the window
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # update the screen
            pygame.display.update(rect_list)

if __name__ == '__main__':
    main()
