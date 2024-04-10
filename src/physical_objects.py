import pygame as pg
from game_parameters import *
from enum import Enum
import math


class WormState(Enum):
    GROUNDED = 0
    AIRBORNE = 1


class Item(Enum):
    PneumaticDrill = 0
    Grenade = 1


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
    bouncingAbsorption = 0.6

    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.deplacementVec = Vector(0, 0)

    def moveFree(self):
        self.deplacementVec.add(self.gravityVector)
        self.handleCollision()
        #print(self.deplacementVec)
        self.x += self.deplacementVec.vx
        self.y += self.deplacementVec.vy

    def handleCollision(self):
        stuckGround = False
        if (self.x + self.radius + self.deplacementVec.vx > GameParameters.XMAX) or (
                self.x - self.radius + self.deplacementVec.vx < GameParameters.XMIN):
            self.deplacementVec.vx = -self.deplacementVec.vx * self.bouncingAbsorption
            self.deplacementVec.vy *= self.bouncingAbsorption

        if (self.y + self.radius + self.deplacementVec.vy > GameParameters.YMAX) or (
                self.y - self.radius + self.deplacementVec.vy < GameParameters.YMIN):
            if (self.y + self.radius + self.deplacementVec.vy > GameParameters.YMAX) and (self.deplacementVec.vy < 2):
                stuckGround = True
            self.deplacementVec.vx *= self.bouncingAbsorption
            self.deplacementVec.vy = -self.deplacementVec.vy * self.bouncingAbsorption

        # colle l'objet au sol
        if stuckGround:
            self.deplacementVec.vx = 0
            self.deplacementVec.vy = 0


class Worm(PhysicalSphere):
    slideSpeed = 4
    radius = 10
    aimAngle = -90
    powerCharge = 0 # a percentage which will be divided by (100/max power)
    hp = 100

    def __init__(self, x, y):
        PhysicalSphere.__init__(self, x, y, 10)
        self.state = WormState.GROUNDED
        self.bouncingAbsorption = 0.4

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
            self.deplacementVec.vy = GameParameters.JUMPPOWER
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
        pg.draw.circle(screen, GameParameters.WORMCOLOR, (self.x, self.y), self.radius)

    import math
    import pygame as pg

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


# class WeaponType(Enum):
#	LAUNCHED = 0
#	Melee = 1
#	Thrown = 2

class Inventory:

    def __init__(self):
        self.selectedItem = 0
        self.items = [Item.PneumaticDrill, Item.Grenade]
        self.sprites = pg.image.load("worms.png")

    def changeSelectedItem(self):
        self.selectedItem = (self.selectedItem + 1) % len(self.items)

    def currentItem(self):
        return self.items[self.selectedItem]

    def triggerCurrentItem(self, worm, objects):
        if self.currentItem() == Item.Grenade:
            grenade = Grenade(worm.x, worm.y, worm.aimAngle, (worm.powerCharge / 10))
            objects.append(grenade)
        elif self.currentItem() == Item.PneumaticDrill:
            pass  # TODO : passer les coordonnées du worms en param


        w1 = PhysicalSphere(worm.x, worm.y, 5)
        w1.deplacementVec.vy = 30
        return w1

    def draw(self, screen):
        y = math.floor((32 * self.selectedItem) / 256)
        x = (32 * self.selectedItem) % 256
        portion_rect = pg.Rect(x, 32 * y, 32, 32)  # (400, 400),
        image_portion = self.sprites.subsurface(portion_rect)
        maxX, maxY = pg.display.get_surface().get_size()
        scaled_image = pg.transform.scale(image_portion, (128, 128))
        screen.blit(scaled_image, (maxX - 128, maxY - 128))


class Utility:
    def __init__(self):
        pass


class PneumaticDrill(Utility):
    def __init__(self):
        Utility.__init__(self)

    def use(self, worm):
        print("Pneumatic drill used")


class Weapon:
    def __init__(self, damage):
        self.damage = damage

    def shot(self, power):
        print("pan pan")


class Grenade(Weapon, PhysicalSphere):
    radius = 8
    bouncingAbsorption = 0.6
    explosionRadius = 60

    def __init__(self, x, y, angle, power):
        Weapon.__init__(self, 50)
        PhysicalSphere.__init__(self, x, y, self.radius)
        power /= 1.3 # divided by 1.3 because max power is 77
        self.deplacementVec.vy = math.sin(math.radians(angle)) * power
        self.deplacementVec.vx = math.cos(math.radians(angle)) * power
        self.creation_tick = pg.time.get_ticks()

    def explode(self, worms):
        for w in worms:
            distance = math.sqrt((w.x - self.x)**2 + (w.y - self.y)**2)
            if distance <= self.explosionRadius:
                w.loseHp(self.damage)

    def draw(self, screen):
        pg.draw.circle(screen, (0, 255, 0), (self.x, self.y), self.radius)
