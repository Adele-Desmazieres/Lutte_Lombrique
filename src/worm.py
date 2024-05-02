import math
import pygame as pg
import numpy as np
from enum import Enum
from physical_sphere import *
from settings import *
from explosive import *
from geometry import *


class Worm(PhysicalSphere, Explosive):
    slideSpeed = 4
    radius = 10
    powerCharge = 0  # a percentage which will be divided by (100/max power)
    maxWalkableSlopeAngle = math.radians(65)
    id = -1

    def __init__(self, x, y, playerIndex):
        PhysicalSphere.__init__(self, x, y, 10)
        self.aimAngle = -90
        self.bouncingAbsorption = 0.4
        self.shouldExplode = True
        self.hp = 100
        self.damage = 10
        self.explosionRadius = 30
        self.image = pg.image.load(Settings.WORM_IMG_PATH)
        self.width = self.radius * 1.5
        self.height = self.image.get_height() * self.width / self.image.get_width()
        self.image = pg.transform.scale(self.image, (self.width, self.height))
        self.playerIndex = playerIndex

    def loseHp(self, damage):
        self.hp -= damage

    def moveRight(self, terrain):
        if self.stuckGround:
            self.x += self.slideSpeed
            self.handleSlidingCollision(terrain)

    def moveLeft(self, terrain):
        if self.stuckGround:
            self.x -= self.slideSpeed
            self.handleSlidingCollision(terrain)

    def handleSlidingCollision(self, terrain):
        # récupère la surface walkable la plus proche
        ls = list(terrain.surfaces)
        best_surface = ls[0]
        best_point = closest_point_on_line(best_surface, (self.x, self.y))

        for surface in ls[1:]:
            point = closest_point_on_line(surface, (self.x, self.y))
            if distance((self.x, self.y), point) < distance((self.x, self.y), best_point):
                best_surface = surface
                best_point = point

        angle = math.pi - best_surface.angle
        if best_surface.angle < 0:
            angle -= 2*math.pi

        # print("Position du worm       : ", self.x, self.y)
        # print("Surface la plus proche : ", best_surface.p, best_surface.q)
        # print("Son angle              : ", math.degrees(best_surface.angle), " deg")
        # print("Son angle corrigé      : ", math.degrees(angle), " deg")
        # print("Sa distance au worm    : ", distance((self.x, self.y), best_point))
        # print("")

        if -self.maxWalkableSlopeAngle <= angle <= self.maxWalkableSlopeAngle:
            x,y = self.moveOnTopOfSurface(best_surface)
            self.x = x
            self.y = y
        else:
            self.stuckGround = False
            self.handleCollision(terrain)

    def moveOnTopOfSurface(self, surface):
        closest_point = closest_point_on_line(surface, (self.x, self.y))
        direction_vector_x = self.x - closest_point[0]
        direction_vector_y = self.y - closest_point[1]

        # print("Vecteur directeur x : ", direction_vector_x)
        # print("Vecteur directeur y : ", direction_vector_y)

        distance = math.sqrt(direction_vector_x ** 2 + direction_vector_y ** 2)
        scale_factor = self.radius / distance
        new_sphere_center_x = closest_point[0] + scale_factor * direction_vector_x
        new_sphere_center_y = closest_point[1] + scale_factor * direction_vector_y
        return (new_sphere_center_x, new_sphere_center_y)

    def jump(self):
        if self.stuckGround:
            self.deplacementVec.vy = -Settings.JUMPPOWER
            self.stuckGround = False

    def aimLeft(self):
        # if self.aimAngle > (-165):
        self.aimAngle -= 1

    def aimRight(self):
        # if self.aimAngle < (-15):
        self.aimAngle += 1

    def charge(self):
        if self.powerCharge < Settings.MAX_POWER_CHARGE:
            self.powerCharge += 2

    def draw(self, view, screen, outline=False):
        # affiche le worm
        x2 = self.x + self.radius - self.width
        y2 = self.y + self.radius - self.height
        if outline:
            view.draw_outline(self.image, (x2, y2))
        screen.blit(self.image, (x2, y2))

        # affiche sa hitbox
        # if self.stuckGround:
        #     pg.draw.circle(screen, (255, 10, 10), (self.x, self.y), self.radius, width=2)
        # else:
        #     pg.draw.circle(screen, (200, 200, 10), (self.x, self.y), self.radius, width=2)

        # affiche les points de vie des worms
        text = view.font_small.render(str(self.hp), True, Settings.HPCOLORS[self.playerIndex])
        textRect = text.get_rect() # create a rectangular object for the text surface object
        textRect.center = (self.x, self.y - self.radius*2) # set the center of the rectangular object
        screen.blit(text, textRect)

    def draw_aiming_cursor(self, screen):
        if self.powerCharge <= 0:
            return None

        color = (250, 100, 10)

        end_x = self.x + math.cos(math.radians(self.aimAngle)) * self.powerCharge
        end_y = self.y + math.sin(math.radians(self.aimAngle)) * self.powerCharge

        start_thickness = 1
        end_thickness = 10

        perpendicular_angle = math.radians(self.aimAngle + 90)
        dx = math.cos(perpendicular_angle)
        dy = math.sin(perpendicular_angle)

        start_left = (self.x - dx * start_thickness / 2, self.y - dy * start_thickness / 2)
        start_right = (self.x + dx * start_thickness / 2, self.y + dy * start_thickness / 2)

        end_left = (end_x - dx * end_thickness / 2, end_y - dy * end_thickness / 2)
        end_right = (end_x + dx * end_thickness / 2, end_y + dy * end_thickness / 2)

        pg.draw.polygon(screen, color, [start_left, start_right, end_right, end_left])

    def draw_line_of_sight(self, screen):
        color = (200, 200, 200, 0.5)

        end_x = self.x + math.cos(math.radians(self.aimAngle)) * Settings.MAX_POWER_CHARGE
        end_y = self.y + math.sin(math.radians(self.aimAngle)) * Settings.MAX_POWER_CHARGE

        start_thickness = 1
        end_thickness = 10

        perpendicular_angle = math.radians(self.aimAngle + 90)
        dx = math.cos(perpendicular_angle)
        dy = math.sin(perpendicular_angle)

        start_left = (self.x - dx * start_thickness / 2, self.y - dy * start_thickness / 2)
        start_right = (self.x + dx * start_thickness / 2, self.y + dy * start_thickness / 2)

        end_left = (end_x - dx * end_thickness / 2, end_y - dy * end_thickness / 2)
        end_right = (end_x + dx * end_thickness / 2, end_y + dy * end_thickness / 2)

        s = pg.Surface((1000,750))
        pg.draw.polygon(screen, color, [start_left, start_right, end_right, end_left])

    def refreshState(self, game):
        if (self.x < Settings.XMIN # Out of map
            or self.x > Settings.XMAX
            or self.y < Settings.YMIN
            or self.y > Settings.YMAX)\
                or self.y > (Settings.YMAX - (Settings.YMAX * (game.numberOfTurns / Settings.MAX_TURNS_NUMBER))): # Under water
            self.hp = 0
            self.shouldExplode = False

    def ejected(self, vec):
        self.deplacementVec = vec
        self.stuckGround = False

