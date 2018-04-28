import pygame
from pygame.locals import *
from random import *
from tkinter import *
import pyBird, pyPipe


pygame.init()
#WINDOW SETUP CONFIG
winTitle = 'Flappy bird'
winHeight = 600
winWidth = 900
window = winHeight*winWidth
FPS = 60 # frames per second setting
fpsClock = pygame.time.Clock()

# set up the window
screen = pygame.display.set_mode((winWidth, winHeight), 0, 32)
pygame.display.set_caption(winTitle)

WHITE = (255, 255, 255)
RED = (255,   0,   0)

activateAI = True
AINeverLose = False
showAISensors = True
AISpeedUp = True
if AISpeedUp and activateAI:
    FPS *= 10

gravity = 9
started = False
gameover = False
mutation = 1
score = 0
hiScore = 0
bird = pyBird.Bird(80,winHeight/2, 10, 10, gravity)

pipeSpace = 0
pipeNum = 4
pipeSpeed = 2

pipes = []
for i in range(0,pipeNum):
    pipes.append(pyPipe.Pipe(winHeight, winWidth + pipeSpace,pipeSpeed))
    pipeSpace += winWidth*0.275


def restart():
    global pipes, pipeSpace, pipeNum, pipeSpeed
    global winHeight, winWidth, started, gameover, score, c
    global bird
    c = 0
    pipes = []
    pipeSpace = 0
    for i in range(0, pipeNum):
        pipes.append(pyPipe.Pipe(winHeight, winWidth + pipeSpace, pipeSpeed))
        pipeSpace += winWidth * 0.275
    bird.y = winHeight/2
    score = 0
    bird.brain.generation += 1
    #print(bird.brain.generation, bird.brain.pipeAware)
    started = False
    gameover = False

age = 0

font = pygame.font.SysFont("comicsansms", 20)

hard = False
c = 0
state = "add"
while True:#Keyrir leikinn

    age += 0.000001
    if bird.brain.sight >= 75:
        bird.brain.sight = bird.brain.sight - age
    screen.fill((round(c), round(c), round(c)))
    scoreText = font.render("Score: " + str(score), True, (0, 128, 255))
    hiscoreText = font.render("Hi-Score: " + str(hiScore), True, (0, 128, 255))
    generationText = font.render("Generation: "+str(bird.brain.generation), True, (0, 128, 255))
    bird.draw(screen)
    for pipe in pipes:
        pipe.draw(screen)
    if started and not gameover:
        if hard:
            if state == "add":
                if c < 255:
                    c += 1
                else:
                    state = "dec"
            else:
                if c > 0:
                    c -= 1
                else:
                    state = "add"
        if activateAI:
            if bird.y + bird.brain.awareness[0] > winHeight:
                bird.react()
        if bird.x + bird.brain.sight >= pipes[0].x:
            if activateAI:
                #print(bird.brain.sensors, pipes[0].gapStart, pipes[0].gapStart + pipes[0].gap)
                if AINeverLose:
                    if bird.y + bird.brain.awareness[0] > pipes[0].gapStart + pipes[0].gap:
                        bird.react()
                if bird.brain.sensors[0] <= pipes[0].gapStart or bird.brain.sensors[2] >= pipes[0].gapStart + pipes[0].gap:
                    if bird.brain.sensors[2] > pipes[0].gapStart:
                        bird.react()
                    if bird.brain.sensors[2] > pipes[0].gapStart + pipes[0].gap:
                        bird.react()
        for pipe in pipes:
            pipe.update()
            if pipe.birdCollision(int(bird.x), int(bird.y), bird.size)[0]:
                #print(bird.brain.sensors)
                if pipe.birdCollision(int(bird.x), int(bird.y), bird.size)[1]:
                    bird.brain.pipeAware[0] += 1 * mutation
                    bird.brain.pipeAware[1] -= 0.5 * mutation
                else:
                    bird.brain.pipeAware[0] += 0.5 * mutation
                    bird.brain.pipeAware[1] -= 1 * mutation
                gameover = True
            elif not gameover:
                gameover = bird.checkBoundaries(0, winHeight)

            if bird.x >= pipe.x+pipe.width/2 and not pipe.scoreGiven:
                score += 1
                pipe.scoreGiven = True
                #print(score)
            if pipe.x + pipe.width < 0:
                pipes.remove(pipe)
                pipes.append((pyPipe.Pipe(winHeight, winWidth, pipeSpeed)))
        bird.applyGravity()
    elif gameover:
        if score > hiScore:
            hiScore = score
        if activateAI:
            restart()
            started = True
    if showAISensors and activateAI:
        #Teikna Sensors
        pygame.draw.line(screen, (0, 255, 0), (bird.x, bird.y), (bird.x + bird.brain.sight, bird.brain.sensors[0]))
        pygame.draw.line(screen, (255, 0, 0), (bird.x, bird.y), (bird.x + bird.brain.sight, bird.brain.sensors[1]))
        pygame.draw.line(screen, (0, 0, 255), (bird.x, bird.y), (bird.x + bird.brain.sight, bird.brain.sensors[2]))
        #Teina Awareness

        pygame.draw.line(screen, (0, 255, 255), (bird.x, bird.y), (bird.x, bird.y + bird.brain.awareness[0]))
        pygame.draw.line(screen, (0, 255, 255), (bird.x, bird.y), (bird.x, bird.y + bird.brain.awareness[1]))

    screen.blit(scoreText, (winWidth - scoreText.get_width(), 0))
    screen.blit(hiscoreText, (winWidth - hiscoreText.get_width(), scoreText.get_height()))
    screen.blit(generationText, (0, winHeight - generationText.get_height()))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if (event.key == K_SPACE):
                if gameover:
                    restart()
                else:
                    if not started:
                        started = True
                    else:
                        bird.jump()
    pygame.display.update()
    fpsClock.tick(FPS)