from random import randint
import pygame
class Pipe:
    def __init__(self, screenHeight, screenEnd, speed):
        self.speed = speed
        self.x = screenEnd
        self.width = 50
        self.screenHeight = screenHeight
        self.gap = 200
        self.gapStart = randint(0,screenHeight-self.gap)
        self.scoreGiven = False

    def draw(self, Surface):
        pygame.draw.rect(Surface,(255, 255, 255),(self.x,0,self.width,self.gapStart),0)
        pygame.draw.rect(Surface, (255, 255, 255), (self.x, self.gapStart+self.gap, self.width, self.screenHeight), 0)

    def update(self):
        self.x -= self.speed

    def birdCollision(self, birdX, birdY, birdSize):
        if birdX in range (int(self.x), int(self.x+self.width)):
            if (birdY < self.gapStart or birdY > self.gapStart+self.gap):
                if birdY < self.gapStart:
                    return (True, 0)
                elif birdY > self.gapStart+self.gap:
                    return (True, 1)
        return (False, 0)