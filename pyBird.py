import pygame
import pyBrain
class Bird:
    def __init__(self,xStart, yStart, size, mass, gravity):
        self.y = yStart
        self.x = xStart
        self.size = size
        self.mass = mass
        self.originaGrav = gravity
        self.gravity = gravity
        self.falling = True
        self.globalTimer = 0
        self.reacting = False

        #Brain stuff
        self.brain = pyBrain.Brain(self.y)

    def update(self):
        self.brain.eyePos = self.y
        self.brain.update()

    def draw(self, pySurface):
        pygame.draw.circle(pySurface, (255, 255, 255), (self.x, int(self.y)), self.size, 0)
        self.update()

    def applyGravity(self):
        if self.falling:
            self.y += round((self.gravity*0.1)*self.mass)
        else:
            if self.globalTimer > 0:
                self.y -= round((self.gravity * 0.1) * self.mass)
                self.globalTimer -= 1
            else:
                self.falling = True

    def jump(self):
        self.falling = False
        self.globalTimer = 10

    def checkBoundaries(self, top, bottom):
        if self.y-self.size < top or self.y+self.size > bottom:
            if self.y+self.size > bottom:
                #print(self.brain.awareness)
                self.brain.awareness[0] += 1
            elif self.y-self.size < top:
                self.brain.awareness[1] -= 1
            return True
        else:
            return False

    def react(self):
        for i in range(0,self.brain.reactionTime):
            if i == self.brain.reactionTime - 1:
                self.jump()