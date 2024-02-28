import sys
import random
import pygame
from pygame.locals import *
def drawFloor():
    screen.blit(floorSurface, (floorXPosition, 826))
    screen.blit(floorSurface, (floorXPosition + 576, 826))
pygame.init()
#screen size
screen = pygame.display.set_mode((576, 950))
#clock - used for setting frame rate
clock = pygame.time.Clock()
#background of game surface, scale up to meet screen
backgroundSurface = pygame.image.load('PNG/background-day.png').convert()
backgroundSurface = pygame.transform.scale2x(backgroundSurface)

Bird = pygame.image.load('PNG/yellowbird-upflap.png').convert()
Bird = pygame.transform.scale2x(Bird)

floorSurface = pygame.image.load('PNG/base.png').convert()
floorSurface = pygame.transform.scale2x(floorSurface)
floorXPosition = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    #put new surfaces on top of display surface
    screen.blit(backgroundSurface,(0,0))
    screen.blit(Bird,(150,500))
    floorXPosition -=1
    drawFloor()
    if floorXPosition <= -576:
        floorXPosition = 0

    pygame.display.update()
    #frame rate is 120 fps
    clock.tick(120)