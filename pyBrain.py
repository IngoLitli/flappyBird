class Brain:
    def __init__(self, eyePos):
        self.sight = 100
        self.lookUp = 0
        self.lookDown = 0
        self.eyePos = eyePos
        self.sensors = [self.eyePos - self.lookUp, self.eyePos, self.eyePos + self.lookDown]
        self.awareness = [0,0]
        self.pipeAware = [0,0]
        self.generation = 0
        self.reactionTime = 5000

    def update(self):
        self.sensors = [int(self.eyePos - self.pipeAware[1]), int(self.eyePos), int(self.eyePos + self.pipeAware[0])]