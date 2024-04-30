import math
import pygame as pg
from weapon import *

class Inventory:

    def __init__(self):
        self.selectedItem = 0
        self.items = [Item.Grenade, Item.Bazooka, Item.Teleport, Item.PneumaticDrill]
        self.itemsSprites = [1, 0, 21, 52]
        self.sprites = pg.image.load("../img/weapons.png")

    def changeSelectedItem(self):
        self.selectedItem = (self.selectedItem + 1) % len(self.items)

    def currentItem(self):
        return self.items[self.selectedItem]

    def triggerCurrentItem(self, worm, objects):
        if self.currentItem() == Item.Grenade:
            grenade = Grenade(worm.x, worm.y, worm.aimAngle, (worm.powerCharge / 10))
            objects.append(grenade)
        elif self.currentItem() == Item.Bazooka:
            bazookaShot = Bazooka(worm.x, worm.y, worm.aimAngle)
            objects.append(bazookaShot)
        elif self.currentItem() == Item.PneumaticDrill:
            pass


        w1 = PhysicalSphere(worm.x, worm.y, 5)
        w1.deplacementVec.vy = 30
        return w1

    def draw(self, screen): # TODO : modifier les images
        sprite = self.itemsSprites[self.selectedItem]
        y = math.floor((32 * sprite) / 256)
        x = (32 * sprite) % 256
        portion_rect = pg.Rect(x, 32 * y, 32, 32)  # (400, 400),
        image_portion = self.sprites.subsurface(portion_rect)
        maxX, maxY = pg.display.get_surface().get_size()
        scaled_image = pg.transform.scale(image_portion, (128, 128))
        screen.blit(scaled_image, (maxX - 128, maxY - 128))
