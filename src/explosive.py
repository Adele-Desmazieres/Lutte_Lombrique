import math
import pygame as pg

from settings import *
from geometry import Vector
import worm

class Explosive:
    explosionRadius = 0
    damage = 0
    projection_force_max = 18
    projection_force_min = 12
    centers = []

    def __init__(self):
        pass

    def explode(self, game, centers):
        self.centers = centers
        self.explode_terrain(game)
        self.explode_worms(game.worms)

    def explode_worms(self, worms):
        for center in self.centers:
            x, y = center
            for w in worms:
                distance = math.sqrt((w.x - self.x) ** 2 + (w.y - self.y) ** 2)
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
                
                # met des vers en chute libre, au cas ou du terrain soit détruit sous eux
                if distance - worm.Worm.radius <= self.explosionRadius*3:
                    w.stuckGround = False

    def explode_terrain(self, game):
        newmap = [[game.map[i][j] for j in range(len(game.map[0]))] for i in range(len(game.map))]

        for i in range(len(game.map)):
            for j in range(len(game.map[0])):
                x = i * Settings.MAP_SQUARE_SIZE
                y = j * Settings.MAP_SQUARE_SIZE

                # Calculer la distance minimale parmi les trois centres
                min_distance = min(math.sqrt((x - cx) ** 2 + (y - cy) ** 2) for cx, cy in self.centers)

                updatelimit = self.explosionRadius + Settings.MAP_SQUARE_SIZE * 2
                if min_distance <= updatelimit:
                    newvalue = min_distance * (Settings.MAP_THRESHOLD + 1) / updatelimit
                    newmap[i][j] = min(newmap[i][j], newvalue)

        game.map = newmap
        game.initTerrain()
        game.view.set_terrain_img(game.view.update_terrain_img(game))
    
    def draw_explosion(screen, position, max_radius, colors):
        num_circles = 10
        clock = pg.time.Clock()
    
        pg.draw.circle(screen, rd.choice(colors), position, max_radius)
    
        for i in range(num_circles):
            if max_radius < 5:
                break
            radius = rd.randint(5, max_radius)
            color = rd.choice(colors)
            pg.draw.circle(screen, color, position, radius)
            max_radius -= 5
            clock.tick(40)
            pg.display.flip()
