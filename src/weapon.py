import math
import pygame as pg
from enum import Enum
from physical_sphere import *

class Item(Enum):
    PneumaticDrill = 0
    Grenade = 1
    Bazooka = 2


# class WeaponType(Enum):
#	Launched = 0
#	Melee = 1
#	Thrown = 2


class Utility:
    def __init__(self):
        pass


class PneumaticDrill(Utility):
    def __init__(self):
        Utility.__init__()

    def use(self, worm):
        print("Pneumatic drill used")


class Weapon:
    def __init__(self, damage):
        self.damage = damage


class Grenade(Weapon, PhysicalSphere):
    radius = 8
    bouncingAbsorption = 0.6
    explosionRadius = 60

    def __init__(self, x, y, angle, power):
        Weapon.__init__(self, 50)
        PhysicalSphere.__init__(self, x, y, self.radius)
        power /= 1.3  # divided by 1.3 because max power is 77
        self.deplacementVec.vy = math.sin(math.radians(angle)) * power
        self.deplacementVec.vx = math.cos(math.radians(angle)) * power
        self.creation_tick = pg.time.get_ticks()

    def explode(self, worms):
        # TODO : appliquer la force de poussée aux worms
        for w in worms:
            distance = math.sqrt((w.x - self.x) ** 2 + (w.y - self.y) ** 2)
            if distance <= self.explosionRadius:
                w.loseHp(self.damage)
                if distance > 0:
                    # TODO : rendre la force proportionnelle à la distance ? force_magnitude = (self.explosionRadius - distance) / self.explosionRadius
                    force_magnitude = 10
                    angle_to_worm = math.atan2(w.y - self.y, w.x - self.x)
                    w.deplacementVec.vx += math.cos(angle_to_worm) * force_magnitude
                    w.deplacementVec.vy += math.sin(angle_to_worm) * force_magnitude


    def draw(self, screen):
        pg.draw.circle(screen, (0, 255, 0), (self.x, self.y), self.radius)

class Bazooka(Weapon, PhysicalSphere):
    radius = 8
    bouncingAbsorption = 0.6
    explosionRadius = 50

    def __init__(self, x, y, angle):
        Weapon.__init__(self, 60)
        PhysicalSphere.__init__(self, x, y, self.radius)
        self.deplacementVec.vy = math.sin(math.radians(angle)) * 30
        self.deplacementVec.vx = math.cos(math.radians(angle)) * 30
        self.collisionDetected = False
        self.collisionPoint = (0, 0)

    def explode(self, worms):
        for w in worms:
            x, y = self.collisionPoint
            distance = math.sqrt((w.x - x) ** 2 + (w.y - y) ** 2)
            if distance <= self.explosionRadius:
                w.loseHp(self.damage)
                if distance > 0:
                    # TODO : rendre la force proportionnelle à la distance ? force_magnitude = (self.explosionRadius - distance) / self.explosionRadius
                    force_magnitude = 10
                    angle_to_worm = math.atan2(w.y - y, w.x - x)
                    w.deplacementVec.vx += math.cos(angle_to_worm) * force_magnitude
                    w.deplacementVec.vy += math.sin(angle_to_worm) * force_magnitude
        # todo : passer le terrain en paramètre et reprendre la même logique pour casser les bouts de terrain

    # TODO cette fonction doit être la copie quasi exacte d'handle collision mais passe X à true si collision
    def handleCollision(self, terrain):
        # TODO : ajouter en arguments les autres worms pour que leurs hitbox soient détéctées comme des collisions ?
        stuckGround = False
        if (self.x + self.radius + self.deplacementVec.vx > Settings.XMAX) or (
                self.x - self.radius + self.deplacementVec.vx < Settings.XMIN):
            self.collisionDetected = True
            self.collisionPoint = (self.x, self.y)
            print("x = {}, y = {} ".format(self.x, self.y))

        if (self.y + self.radius + self.deplacementVec.vy > Settings.YMAX) or (
                self.y - self.radius + self.deplacementVec.vy < Settings.YMIN):
            self.collisionDetected = True
            self.collisionPoint = (self.x, self.y)


        for surface in terrain.surfaces:
            if self.intersects(surface):
                self.collisionDetected = True
                self.collisionPoint = (self.x, self.y)
                break

        if stuckGround:
            self.deplacementVec.vx = 0
            self.deplacementVec.vy = 0

    def draw(self, screen):
        pg.draw.circle(screen, (255, 0, 0), (self.x, self.y), self.radius)
