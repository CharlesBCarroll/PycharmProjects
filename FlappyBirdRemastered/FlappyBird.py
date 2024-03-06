import sys
import random
import pygame
from pygame.locals import *
def drawFloor():
    screen.blit(floorSurface, (floorXPosition, 826))
    screen.blit(floorSurface, (floorXPosition + 576, 826))
def createPipe():
    randomPipePos = random.choice(pipeHeight)
    newPipe = pipeSurface.get_rect(midtop = (700,randomPipePos))
    return newPipe
def MovePipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes
def DrawPipes(pipes):
    for pipe in pipes:
        screen.blit(pipeSurface, pipe)

pygame.init()
#screen size
screen = pygame.display.set_mode((576, 950))
#clock - used for setting frame rate
clock = pygame.time.Clock()

gravity = 0.25
BirdMovement = 0

#background of game surface, scale up to meet screen
backgroundSurface = pygame.image.load('PNG/background-day.png').convert()
backgroundSurface = pygame.transform.scale2x(backgroundSurface)

#Adds bird to surface, scales up, puts rectangle around it for collision
Bird = pygame.image.load('PNG/yellowbird-midflap.png').convert()
Bird = pygame.transform.scale2x(Bird)
BirdRect = Bird.get_rect(center=(100,475))

#Floor surface, floor x position is 0, allows for movement of floor in loop
floorSurface = pygame.image.load('PNG/base.png').convert()
floorSurface = pygame.transform.scale2x(floorSurface)
floorXPosition = 0

pipeSurface = pygame.image.load('PNG/pipe-green.png')
pipeSurface = pygame.transform.scale2x(pipeSurface)
pipeList = []
CREATEpIPE = pygame.USEREVENT
pygame.time.set_timer(CREATEpIPE,1200)
pipeHeight = [400,600,800]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        #allows for movement upward on space press, resets gravity every press
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                BirdMovement = 0
                BirdMovement -= 8
        if event.type == CREATEpIPE:
            pipeList.append(createPipe())

    #put new surfaces on top of display surface
    screen.blit(backgroundSurface,(0,0))
    #adds gravity as fall, movement comes from center of the rectangle
    BirdMovement += gravity
    BirdRect.centery += BirdMovement
    #creates bird and the rectangle around the bird to check for collisions
    screen.blit(Bird,BirdRect)

    #Pipes
    pipeList = MovePipes(pipeList)
    DrawPipes(pipeList)



    floorXPosition -=1
    drawFloor()
    if floorXPosition <= -576:
        floorXPosition = 0

    pygame.display.update()
    #frame rate is 120 fps
    clock.tick(120)