import sys
import random
import pygame
from pygame.locals import *
def drawFloor():
    screen.blit(floorSurface, (floorXPosition, 826))
    screen.blit(floorSurface, (floorXPosition + 576, 826))

def createPipe():
    randomPipePos = random.choice(pipeHeight)
    BottomPipe = pipeSurface.get_rect(midtop=(700, randomPipePos))
    TopPipe = pipeSurface.get_rect(midbottom=(700, randomPipePos - 300))
    return BottomPipe, TopPipe

def movePipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes

def drawPipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 1024:
            screen.blit(pipeSurface, pipe)
        else:
            flipPipe = pygame.transform.flip(pipeSurface, False, True)
            screen.blit(flipPipe, pipe)

def checkCollision(pipes):
    for pipe in pipes:
        if birdRect.colliderect(pipe):
            return True
    if birdRect.top <= -100 or birdRect.bottom >= 826:
        return True
    return False

def rotateBird(bird):
    newBird = pygame.transform.rotozoom(bird, -birdMovement * 3, 1)
    return newBird

def birdAnimation():
    newBird = birdFrames[birdIndex]
    newBirdrect = newBird.get_rect(center=(288, birdRect.centery))
    return newBird, newBirdrect

def scoreDisplay(gameState):
    if gameState == 'mainGame':
        scoreSurface = gameFont.render(str(int(score)), True, (255, 255, 255))
        scoreRect = scoreSurface.get_rect(center=(288, 100))
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
# screen size
screen = pygame.display.set_mode((576, 950))
# clock - used for setting frame rate
clock = pygame.time.Clock()
gameFont = pygame.font.Font('04B_19 (1).TTF', 40)

# game variables
gravity = 0.35
birdMovement = 0
score = 0
highScore = 0

# background of game surface, scale up to meet screen
backgroundSurface = pygame.image.load('PNG/background-day.png').convert()
backgroundSurface = pygame.transform.scale2x(backgroundSurface)

backgroundSurface2 = pygame.image.load('PNG/background-night.png').convert()
backgroundSurface2 = pygame.transform.scale2x(backgroundSurface2)

birdDownFlap = pygame.transform.scale2x(pygame.image.load('PNG/yellowbird-downflap.png').convert_alpha())
birdUpFlap = pygame.transform.scale2x(pygame.image.load('PNG/yellowbird-upflap.png').convert_alpha())
birdMidFlap = pygame.transform.scale2x(pygame.image.load('PNG/yellowbird-midflap.png').convert_alpha())
birdFrames = [birdDownFlap, birdUpFlap, birdMidFlap]
birdIndex = 0
bird = birdFrames[birdIndex]
birdRect = bird.get_rect(center=(288, 475))
birdFlapEvent = pygame.USEREVENT + 1

# Floor surface, floor x position is 0, allows for movement of floor in loop
floorSurface = pygame.image.load('PNG/base.png').convert()
floorSurface = pygame.transform.scale2x(floorSurface)
floorXPosition = 0

pipeSurfaceGreen = pygame.image.load('PNG/pipe-green.png')
pipeSurfaceGreen = pygame.transform.scale2x(pipeSurfaceGreen)

pipeSurfaceRed = pygame.image.load('PNG/pipe-red.png')
pipeSurfaceRed = pygame.transform.scale2x(pipeSurfaceRed)

pipeSurface = pipeSurfaceGreen


pipeList = []
createPipeEvent = pygame.USEREVENT
pipe_creation_interval = 1500
pygame.time.set_timer(createPipeEvent, pipe_creation_interval)
pipeHeight = [400, 600, 800]

# Load game over surface
gameOverSurface = pygame.transform.scale2x(pygame.image.load('PNG/gameover.png').convert_alpha())
gameOverRect = gameOverSurface.get_rect(center=(288, 475))

# Load new game surface
newGameSurface = pygame.transform.scale2x(pygame.image.load('PNG/message.png').convert_alpha())
newGameRect = newGameSurface.get_rect(center=(288, 380))

gameStates = {"START": 0, "ACTIVE": 1, "GAME_OVER": 2}
currentState = gameStates["START"]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if currentState == gameStates["START"]:
                    currentState = gameStates["ACTIVE"]
                    birdRect.center = (288, 475)
                    pipeList.clear()
                    birdMovement = 0
                    score = 0
                    pygame.time.set_timer(birdFlapEvent, 200)
                elif currentState == gameStates["ACTIVE"]:
                    birdMovement = 0
                    birdMovement -= 8
                elif currentState == gameStates["GAME_OVER"]:
                    currentState = gameStates["START"]

        if event.type == createPipeEvent:
            if currentState == gameStates["ACTIVE"]:
                pipeList.extend(createPipe())
        if event.type == birdFlapEvent:
            if currentState == gameStates["ACTIVE"]:
                if birdIndex < 2:
                    birdIndex += 1
                else:
                    birdIndex = 0
                bird, birdRect = birdAnimation()


    screen.blit(backgroundSurface, (0, 0))
    if score >=2:
        screen.blit(backgroundSurface2, (0,0))

    if currentState == gameStates["START"]:
        pipe_creation_interval = 1700
        pygame.time.set_timer(createPipeEvent, pipe_creation_interval)
        pipeSurface = pipeSurfaceGreen
        screen.blit(backgroundSurface, (0,0))
        screen.blit(newGameSurface, newGameRect)
        screen.blit(bird, birdRect)
        birdRect.center = (288, 475)
        pygame.time.set_timer(birdFlapEvent, 0)
    elif currentState == gameStates["ACTIVE"]:
        birdMovement += gravity
        rotatedBird = rotateBird(bird)
        birdRect.centery += birdMovement
        screen.blit(rotatedBird, birdRect)
        active = not checkCollision(pipeList)
        pipeList = movePipes(pipeList)
        drawPipes(pipeList)

        for pipe in pipeList:
            if pipe.centerx == 100:
                score += 1
                if score >= 2:
                    pipe_creation_interval = 1400
                    pygame.time.set_timer(createPipeEvent, pipe_creation_interval)
                    pipeSurface = pipeSurfaceRed
                    if score >= 15:
                        pipeSurface = pipeSurfaceRed
                        if score >= 20:
                            pipe_creation_interval = 1000
                            pygame.time.set_timer(createPipeEvent, pipe_creation_interval)
                            if score >=30:
                                pipe_creation_interval = 700
                                pygame.time.set_timer(createPipeEvent, pipe_creation_interval)

                break
        scoreDisplay('mainGame')

        if not active:
            currentState = gameStates["GAME_OVER"]
            pygame.time.set_timer(birdFlapEvent, 0)

    elif currentState == gameStates["GAME_OVER"]:
        screen.blit(gameOverSurface, gameOverRect)
        highScore = updateScore(score, highScore)
        scoreDisplay('gameOver')

    drawFloor()
    floorXPosition -= 1
    if floorXPosition <= -576:
        floorXPosition = 0

    pygame.display.update()
    clock.tick(80)
