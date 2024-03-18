import sys
import random
import pygame
from pygame.locals import *
def drawFloor():
    screen.blit(floorSurface, (floorXPosition, 826))
    screen.blit(floorSurface, (floorXPosition + 576, 826))
def createPipe():
    randomPipePos = random.choice(pipeHeight)
    BottomPipe = pipeSurface.get_rect(midtop = (700,randomPipePos))
    TopPipe = pipeSurface.get_rect(midbottom = (700,randomPipePos - 300))
    return BottomPipe, TopPipe
def MovePipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes
def DrawPipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 1024:
                screen.blit(pipeSurface, pipe)
        else:
            flipPipe = pygame.transform.flip(pipeSurface, False, True)
            screen.blit(flipPipe, pipe)
def CheckCollision(pipes):
    for pipe in pipes:
        if BirdRect.colliderect(pipe):
            return False
    if BirdRect.top <= -100 or BirdRect.bottom >= 826:
        return False
    return True
def rotateBird(bird):
    newBird = pygame.transform.rotozoom(bird,-BirdMovement*3, 1)
    return newBird
def birdAnimation():
    newBird = BirdFrames[BirdIndex]
    newBirdrect = newBird.get_rect(center = (100,BirdRect.centery))
    return newBird,newBirdrect
def scoreDisplay(gameState):
    if gameState == 'mainGame':
        scoreSurface = gameFont.render(str(int(score)),True,(255,255,255))
        scoreRect = scoreSurface.get_rect(center= (288,100))
        screen.blit(scoreSurface, scoreRect)
    if gameState == 'gameOver':
        scoreSurface = gameFont.render(f'Score: {int(score)}', True, (255, 255, 255))
        scoreRect = scoreSurface.get_rect(center=(288, 100))
        screen.blit(scoreSurface, scoreRect)

        highScoreSurface = gameFont.render(f'High Score: {int(highScore)}', True, (255, 255, 255))
        highScoreRect = highScoreSurface.get_rect(center=(288, 800))
        screen.blit(highScoreSurface, highScoreRect)
def updateScore(score, highScore):
    if score > highScore:
        highScore = score
    return highScore


pygame.init()
#screen size
screen = pygame.display.set_mode((576, 950))
#clock - used for setting frame rate
clock = pygame.time.Clock()
gameFont = pygame.font.Font('04B_19 (1).TTF',40)

#game variables
gravity = 0.25
BirdMovement = 0
ActiveGame = True
score = 0
highScore = 0

#background of game surface, scale up to meet screen
backgroundSurface = pygame.image.load('PNG/background-day.png').convert()
backgroundSurface = pygame.transform.scale2x(backgroundSurface)

BirdDownFlap = pygame.transform.scale2x(pygame.image.load('PNG/yellowbird-downflap.png').convert_alpha())
BirdUpFlap = pygame.transform.scale2x(pygame.image.load('PNG/yellowbird-upflap.png').convert_alpha())
BirdMidFlap = pygame.transform.scale2x(pygame.image.load('PNG/yellowbird-midflap.png').convert_alpha())
BirdFrames = [BirdDownFlap, BirdUpFlap, BirdMidFlap]
BirdIndex = 1
Bird = BirdFrames[BirdIndex]
BirdRect = Bird.get_rect(center=(100,475))
BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

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

gameOverSurface = pygame.transform.scale2x(pygame.image.load('PNG/gameover.png').convert_alpha())
gameOverRect = gameOverSurface.get_rect(center=(288,375))

newGameSurface = pygame.transform.scale2x(pygame.image.load('PNG/message.png').convert_alpha())
newGameRect = gameOverSurface.get_rect(center=(288,255))

passedPipe = False
restartGame = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        #allows for movement upward on space press, resets gravity every press
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and ActiveGame:
                BirdMovement = 0
                BirdMovement -= 8
            if event.key == pygame.K_SPACE and ActiveGame == False:
                ActiveGame = True
                pipeList.clear()
                BirdRect.center = (100,475)
                BirdMovement = 0
                score = 0
                passedPipe = False
        if event.type == CREATEpIPE:
            pipeList.extend(createPipe())
            passedPipe = False
        if event.type == BIRDFLAP:
            if BirdIndex < 2:
                BirdIndex +=1
            else:
                BirdIndex = 0
            Bird,BirdRect = birdAnimation()

    #put new surfaces on top of display surface
    screen.blit(backgroundSurface,(0,0))

    if ActiveGame:
        screen.blit(newGameSurface,newGameRect)
        #adds gravity as fall, movement comes from center of the rectangle
        BirdMovement += gravity
        rotatedBird = rotateBird(Bird)
        BirdRect.centery += BirdMovement
        #creates bird and the rectangle around the bird to check for collisions
        screen.blit(rotatedBird,BirdRect)
        ActiveGame = CheckCollision(pipeList)
        #Pipes
        pipeList = MovePipes(pipeList)
        DrawPipes(pipeList)

        if not passedPipe:
            for pipe in pipeList:
                if pipe.centerx == 100:
                    passedPipe = True
                    score +=1
                    break
        scoreDisplay('mainGame')
    else:
        screen.blit(gameOverSurface,gameOverRect)
        highScore = updateScore(score, highScore)
        scoreDisplay('gameOver')

    floorXPosition -=1
    drawFloor()
    if floorXPosition <= -576:
        floorXPosition = 0

    pygame.display.update()
    #frame rate is 120 fps
    clock.tick(120)