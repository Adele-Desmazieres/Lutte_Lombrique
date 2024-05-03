import math
import pygame as pg
from enum import Enum
from physical_sphere import *
from geometry import *
from explosive import *

class Item(Enum):
    Grenade = 0
    Bazooka = 1
    Teleporter = 2
    PneumaticDrill = 3

# class WeaponType(Enum):
#	Launched = 0
#	Melee = 1
#	Thrown = 2


class Utility:
    def __init__(self):
        pass

class Teleporter(Utility):
    def __init__(self):
        Utility.__init__(self)

    def teleport(self, x, y, worm):
        worm.x = x
        worm.y = y


class PneumaticDrill(Utility, PhysicalSphere, Explosive):
    radius = 8
    bouncingAbsorption = 0.6
    explosionRadius = 10
    projection_force_max = 2 # Force minimale pour faire tomber le vers (qui autrement ne bouge pas si du terrain est détruit sous ses "pieds")
    projection_force_min = 1
    nbExplosions = 15

    def __init__(self, x, y, angle, power):
        Utility.__init__(self)
        PhysicalSphere.__init__(self, x, y, self.radius)
        self.angle = angle
        power = power / 5
        self.deplacementVec.vy = math.sin(math.radians(angle)) * power
        self.deplacementVec.vx = math.cos(math.radians(angle)) * power
        self.collisionDetected = False
        self.collisionPoint = (0, 0)

    def handleCollision(self, terrain):
        stuckGround = False
        if (self.x + self.radius + self.deplacementVec.vx > Settings.XMAX) or (
                self.x - self.radius + self.deplacementVec.vx < Settings.XMIN):
            self.collisionDetected = True
            self.collisionPoint = (self.x, self.y)

        if (self.y + self.radius + self.deplacementVec.vy > Settings.YMAX) or (
                self.y - self.radius + self.deplacementVec.vy < Settings.YMIN):
            self.collisionDetected = True
            self.collisionPoint = (self.x, self.y)

        for surface in terrain.surfaces:
            if self.line_intersect(self.deplacementVec, surface):
                self.collisionDetected = True
                self.collisionPoint = (self.x, self.y)
                break

        if stuckGround:
            self.deplacementVec.vx = 0
            self.deplacementVec.vy = 0


    def draw(self, screen):
        pg.draw.circle(screen, (150, 10, 150), (self.x, self.y), self.radius)


class Weapon:
    def __init__(self, damage):
        self.damage = damage
    

class Grenade(Weapon, PhysicalSphere, Explosive):
    radius = 8
    bouncingAbsorption = 0.6
    explosionRadius = 60
    projection_force_max = 18
    projection_force_min = 12

    def __init__(self, x, y, angle, power):
        Weapon.__init__(self, 50)
        PhysicalSphere.__init__(self, x, y, self.radius)
        power = power / 10
        self.deplacementVec.vy = math.sin(math.radians(angle)) * power
        self.deplacementVec.vx = math.cos(math.radians(angle)) * power
        self.creation_tick = pg.time.get_ticks()

    def draw(self, screen):
        pg.draw.circle(screen, (0, 255, 0), (self.x, self.y), self.radius)

class Bazooka(Weapon, PhysicalSphere, Explosive):
    radius = 8
    bouncingAbsorption = 0.6
    explosionRadius = 50

    def __init__(self, x, y, angle, power):
        Weapon.__init__(self, 80)
        PhysicalSphere.__init__(self, x, y, self.radius)
        power = power / 6
        self.deplacementVec.vy = math.sin(math.radians(angle)) * power
        self.deplacementVec.vx = math.cos(math.radians(angle)) * power
        self.collisionDetected = False
        self.collisionPoint = (0, 0)

    def handleCollision(self, terrain):
        stuckGround = False
        
        if (self.x + self.radius + self.deplacementVec.vx > Settings.XMAX) or (
                self.x - self.radius + self.deplacementVec.vx < Settings.XMIN):
            self.collisionDetected = True
            self.collisionPoint = (self.x, self.y)

        elif (self.y + self.radius + self.deplacementVec.vy > Settings.YMAX) or (
                self.y - self.radius + self.deplacementVec.vy < Settings.YMIN):
            self.collisionDetected = True
            self.collisionPoint = (self.x, self.y)
            
        else:
            for surface in terrain.surfaces:
                if self.line_intersect(self.deplacementVec, surface):
                    self.collisionDetected = True
                    self.collisionPoint = (self.x, self.y)
                    break

        if stuckGround:
            self.deplacementVec.vx = 0
            self.deplacementVec.vy = 0

    def draw(self, screen):
        pg.draw.circle(screen, (255, 0, 0), (self.x, self.y), self.radius)
