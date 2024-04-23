import math
import pygame as pg
from enum import Enum
from physical_sphere import *
from geometry import *

class Item(Enum):
    PneumaticDrill = 0
    Grenade = 1


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
    projection_force_max = 18
    projection_force_min = 12

    def __init__(self, x, y, angle, power):
        Weapon.__init__(self, 50)
        PhysicalSphere.__init__(self, x, y, self.radius)
        power /= 1.3  # divided by 1.3 because max power is 77
        self.deplacementVec.vy = math.sin(math.radians(angle)) * power
        self.deplacementVec.vx = math.cos(math.radians(angle)) * power
        self.creation_tick = pg.time.get_ticks()

    def explode(self, game):
        self.explode_worms(game.worms)
        self.explode_terrain(game)
            
    def explode_worms(self, worms):
        for w in worms:
            distance = math.sqrt((w.x - self.x) ** 2 + (w.y - self.y) ** 2)
            if distance <= self.explosionRadius:
                x = self.x
                y = self.y + self.radius
                
                # perd des points de vie
                w.loseHp(self.damage)
                
                # se fait propulser par la force de l'explosion
                # calcul de l'angle par trigonométrie
                adj = x - w.x if x != w.x else 1
                opp = y - w.y
                projection_angle = math.atan(opp/adj)
                if w.x < x and w.y < y:
                    projection_angle = math.pi + projection_angle
                elif w.x < x:
                    projection_angle = math.pi - projection_angle
                elif w.y < y:
                    projection_angle = 2*math.pi - projection_angle
                
                # force de propulsion inversement proportionnelle à la distance à l'explosion
                m = (self.projection_force_max - self.projection_force_min) / (-self.explosionRadius)
                n = self.projection_force_max
                projection_force = m * distance + n
                
                vx = projection_force * math.cos(projection_angle)
                vy = projection_force * math.sin(projection_angle)
                print(vx, vy)
                w.ejected(Vector(vx, vy))
        
    def explode_terrain(self, game):
        newmap = [[game.map[i][j] for j in range(len(game.map[0]))] for i in range(len(game.map))]
        for i in range(len(game.map)):
            for j in range(len(game.map[0])):
                x = i * Settings.MAP_SQUARE_SIZE
                y = j * Settings.MAP_SQUARE_SIZE
                distance = math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)
                
                updatelimit = self.explosionRadius + Settings.MAP_SQUARE_SIZE*2 + 5
                if distance <= updatelimit and newmap[i][j] >= Settings.MAP_THRESHOLD:
                    newvalue = distance * (Settings.MAP_THRESHOLD+1) / updatelimit
                    newmap[i][j] = min(newmap[i][j], newvalue)
                    
        game.map = newmap
        game.initTerrain()
        game.view.update_terrain_img(game)
    
    def draw(self, screen):
        pg.draw.circle(screen, (0, 255, 0), (self.x, self.y), self.radius)
