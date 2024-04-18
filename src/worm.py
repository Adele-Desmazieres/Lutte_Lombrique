import math
import pygame as pg
from enum import Enum
from physical_sphere import *
from settings import *

class WormState(Enum):
    GROUNDED = 0
    AIRBORNE = 1


class Worm(PhysicalSphere):
    slideSpeed = 4
    radius = 10
    aimAngle = -90
    powerCharge = 0  # a percentage which will be divided by (100/max power)

    def __init__(self, x, y):
        PhysicalSphere.__init__(self, x, y, 10)
        self.state = WormState.GROUNDED
        self.bouncingAbsorption = 0.4
        self.hp = 100

    def loseHp(self, damage):
        self.hp -= damage

    def moveRight(self):
        if self.state == WormState.GROUNDED:
            self.x += self.slideSpeed

    def moveLeft(self):
        if self.state == WormState.GROUNDED:
            self.x -= self.slideSpeed

    def jump(self):
        if self.state == WormState.GROUNDED:
            self.deplacementVec.vy = Settings.JUMPPOWER
            self.state = WormState.AIRBORNE

    def aimLeft(self):
        if self.aimAngle > (-165):
            self.aimAngle -= 1

    def aimRight(self):
        if self.aimAngle < (-15):
            self.aimAngle += 1

    def charge(self):
        if self.powerCharge < 100:
            self.powerCharge += 2

    def draw(self, screen):
        pg.draw.circle(screen, Settings.WORMCOLOR, (self.x, self.y), self.radius)
        pg.draw.circle(screen, (10, 10, 10), (self.x, self.y), self.radius, width=2)

    def draw_aiming_cursor(self, screen):
        if self.powerCharge <= 0:
            return

        color = (255, 255, 255)

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

    def refreshState(self):
        if True:  # TODO : si on touche le sol, collision avec le terrain
            self.state = WormState.GROUNDED
        else:
            self.state = WormState.AIRBORNE
