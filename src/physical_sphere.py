from settings import *
from geometry import *


class PhysicalSphere:
    gravityVector = Vector(0, Settings.GRAVITY)
    bouncingAbsorption = 0.6

    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.deplacementVec = Vector(0, 0)

    def moveFree(self):
        self.deplacementVec.add(self.gravityVector)
        self.handleCollision()
        # print(self.deplacementVec)
        self.x += self.deplacementVec.vx
        self.y += self.deplacementVec.vy

    def handleCollision(self):
        stuckGround = False
        if (self.x + self.radius + self.deplacementVec.vx > Settings.XMAX) or (
                self.x - self.radius + self.deplacementVec.vx < Settings.XMIN):
            self.deplacementVec.vx = -self.deplacementVec.vx * self.bouncingAbsorption
            self.deplacementVec.vy *= self.bouncingAbsorption

        if (self.y + self.radius + self.deplacementVec.vy > Settings.YMAX) or (
                self.y - self.radius + self.deplacementVec.vy < Settings.YMIN):
            if (self.y + self.radius + self.deplacementVec.vy > Settings.YMAX) and (self.deplacementVec.vy < 2):
                stuckGround = True
            self.deplacementVec.vx *= self.bouncingAbsorption
            self.deplacementVec.vy = -self.deplacementVec.vy * self.bouncingAbsorption

        # TODO : gérer collisions avec le terrain

        # colle l'objet au sol
        if stuckGround:
            self.deplacementVec.vx = 0
            self.deplacementVec.vy = 0


