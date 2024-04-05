from game_parameters import *
from enum import Enum


class WormState(Enum):
    GROUNDED = 0
    AIRBORNE = 1


class Vector:

    def __init__(self, vx, vy):
        self.vx = vx
        self.vy = vy

    def add(self, v):
        self.vx += v.vx
        self.vy += v.vy

    def __str__(self):
        return "(" + str(self.vx) + ", " + str(self.vy) + ")"


class PhysicalSphere:
    gravityVector = Vector(0, GameParameters.GRAVITY)

    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.deplacementVec = Vector(0, 0)

    def moveFree(self):
        self.deplacementVec.add(self.gravityVector)
        self.handleCollision()
        print(self.deplacementVec)
        self.x += self.deplacementVec.vx
        self.y += self.deplacementVec.vy

    def handleCollision(self):
        stuckGround = False
        if (self.x + self.radius + self.deplacementVec.vx > GameParameters.XMAX) or (
                self.x - self.radius + self.deplacementVec.vx < GameParameters.XMIN):
            self.deplacementVec.vx = -self.deplacementVec.vx * GameParameters.BOUNCINGABSORPTION
            self.deplacementVec.vy *= GameParameters.BOUNCINGABSORPTION

        if (self.y + self.radius + self.deplacementVec.vy > GameParameters.YMAX) or (
                self.y - self.radius + self.deplacementVec.vy < GameParameters.YMIN):
            if (self.y + self.radius + self.deplacementVec.vy > GameParameters.YMAX) and (self.deplacementVec.vy < 2):
                stuckGround = True
            self.deplacementVec.vx *= GameParameters.BOUNCINGABSORPTION
            self.deplacementVec.vy = -self.deplacementVec.vy * GameParameters.BOUNCINGABSORPTION

        # colle l'objet au sol
        if stuckGround:
            self.deplacementVec.vx = 0
            self.deplacementVec.vy = 0


class Worm(PhysicalSphere):
    slideSpeed = 4
    radius = 10

    def __init__(self, x, y):
        PhysicalSphere.__init__(self, x, y, 10)
        self.state = WormState.GROUNDED

    def moveRight(self):
        if self.state == WormState.GROUNDED:
            self.x += self.slideSpeed

    def moveLeft(self):
        if self.state == WormState.GROUNDED:
            self.x -= self.slideSpeed

    def jump(self):
        if self.state == WormState.GROUNDED:
            self.deplacementVec.vy = GameParameters.JUMPPOWER
            self.state = WormState.AIRBORNE

    def refreshState(self):
        if True:  # TODO : si on touche le sol
            self.state = WormState.GROUNDED
        else:
            self.state = WormState.AIRBORNE


# class WeaponType(Enum):
#	LAUNCHED = 0
#	Melee = 1
#	Thrown = 2

class Utility:
    def __init__(self):
        pass

class PneumaticDrill(Utility):
    def __init__(self):
        Utility.__init__(self)

    def use(self):
        pass

class Weapon:
    def __init__(self, damage):
        self.damage = damage

    def shot(self, power):
        pass  # TODO


class Grenade(Weapon):
    def __init__(self):
        Weapon.__init__(self, 50)
