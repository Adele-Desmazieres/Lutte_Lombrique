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
    explosionRadius = 20
    projection_force_max = 2 # Force minimale pour faire tomber le vers (qui autrement ne bouge pas si du terrain est détruit sous ses "pieds")
    projection_force_min = 1

    def __init__(self, x, y, angle):
        Utility.__init__(self)
        PhysicalSphere.__init__(self, x, y, self.radius)
        self.angle = angle
        self.deplacementVec.vy = math.sin(math.radians(angle)) * 30
        self.deplacementVec.vx = math.cos(math.radians(angle)) * 30
        self.collisionDetected = False
        self.collisionPoint = (0, 0)
        self.centers = []

    def handleCollision(self, terrain):
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
            if self.line_intersect(self.deplacementVec, surface):
                self.collisionDetected = True
                self.collisionPoint = (self.x, self.y)
                break

        if stuckGround:
            self.deplacementVec.vx = 0
            self.deplacementVec.vy = 0

    def explode_worms(self, worms):
        for center in self.centers:
            x, y = center
            for w in worms:
                w.stuckGround = False
                distance = math.sqrt((w.x - self.x) ** 2 + (w.y - self.y) ** 2)
                if distance <= self.explosionRadius:
                    #y = self.y + self.radius

                    # se fait propulser par la force de l'explosion
                    # calcul de l'angle par trigonométrie
                    adj = x - w.x if x != w.x else 1
                    opp = y - w.y
                    projection_angle = math.atan(opp / adj)
                    if w.x < x and w.y < y:
                        projection_angle = math.pi + projection_angle
                    elif w.x < x:
                        projection_angle = math.pi - projection_angle
                    elif w.y < y:
                        projection_angle = 2 * math.pi - projection_angle

                    # force de propulsion inversement proportionnelle à la distance à l'explosion
                    m = (self.projection_force_max - self.projection_force_min) / (-self.explosionRadius)
                    n = self.projection_force_max
                    projection_force = m * distance + n

                    vx = projection_force * math.cos(projection_angle)
                    vy = projection_force * math.sin(projection_angle)
                    w.ejected(Vector(vx, vy))

    def explode_terrain(self, game):
        newmap = [[game.map[i][j] for j in range(len(game.map[0]))] for i in range(len(game.map))]
        dx = self.explosionRadius * math.cos(math.radians(self.angle))
        dy = self.explosionRadius * math.sin(math.radians(self.angle))
        cX, cY = self.collisionPoint
        self.centers = [(cX, cY),
                   (cX + dx, cY + dy),
                   (cX + 2 * dx, cY + 2 * dy)]

        for i in range(len(game.map)):
            for j in range(len(game.map[0])):
                x = i * Settings.MAP_SQUARE_SIZE
                y = j * Settings.MAP_SQUARE_SIZE

                # Calculer la distance minimale parmi les trois centres
                min_distance = min(math.sqrt((x - cx) ** 2 + (y - cy) ** 2) for cx, cy in self.centers)

                updatelimit = self.explosionRadius + Settings.MAP_SQUARE_SIZE * 2
                if min_distance <= updatelimit and newmap[i][j] >= Settings.MAP_THRESHOLD:
                    newvalue = min_distance * (Settings.MAP_THRESHOLD + 1) / updatelimit
                    newmap[i][j] = min(newmap[i][j], newvalue)

        game.map = newmap
        game.initTerrain()
        game.view.set_terrain_img(game.view.update_terrain_img(game))

    def draw(self, screen):
        for center in self.centers:
            x, y = center
            # print("({}, {})".format(x, y))
            pg.draw.circle(screen, (255, 0, 0), center, self.radius)


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
        Weapon.__init__(self, 60)
        PhysicalSphere.__init__(self, x, y, self.radius)
        power = power / 6
        self.deplacementVec.vy = math.sin(math.radians(angle)) * power
        self.deplacementVec.vx = math.cos(math.radians(angle)) * power
        self.collisionDetected = False
        self.collisionPoint = (0, 0)

    def explode_worms(self, worms):
        x, y = self.collisionPoint
        for w in worms:
            distance = math.sqrt((w.x - x) ** 2 + (w.y - y) ** 2)
            if distance <= self.explosionRadius:
                # perd des points de vie
                w.loseHp((int)(self.damage * (1 - distance / self.explosionRadius)))

                # se fait propulser par la force de l'explosion
                # calcul de l'angle par trigonométrie
                adj = x - w.x if x != w.x else 1
                opp = y - w.y
                projection_angle = math.atan(opp / adj)
                if w.x < x and w.y < y:
                    projection_angle = math.pi + projection_angle
                elif w.x < x:
                    projection_angle = math.pi - projection_angle
                elif w.y < y:
                    projection_angle = 2 * math.pi - projection_angle

                # force de propulsion inversement proportionnelle à la distance à l'explosion
                m = (self.projection_force_max - self.projection_force_min) / (-self.explosionRadius)
                n = self.projection_force_max
                projection_force = m * distance + n

                vx = projection_force * math.cos(projection_angle)
                vy = projection_force * math.sin(projection_angle)
                w.ejected(Vector(vx, vy))

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
