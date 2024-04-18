#!/usr/bin/python3

import pygame as pg
import os
from PIL import Image, ImageDraw
from settings import *
from terrain import *
from worm import *
from map2D import *
from weapon import *
from inventory import *
from explosion import *
from model import *


TERRAIN_IMG = None
PG_TERRAIN_IMG = None


def draw(screen, game):
    screen.fill(Settings.BACKGROUNDCOLOR)
    screen.blit(PG_TERRAIN_IMG, (0,0))
            
    for s in game.terrain.surfaces:
        pg.draw.line(screen, (200, 200, 200), s.p, s.q, width=3)

    for w in game.worms:
        w.moveFree()
        w.draw(screen)

    for o in game.objects:
        o.moveFree()
        o.draw(screen)

    if (game.inventoryOpenState == InventoryState.Opened):
        game.inventory.draw(screen)

    if game.inventory.currentItem() in game.rangedWeapons:
        game.worms[game.current_worm_id].draw_aiming_cursor(screen)

    pg.display.flip()


def initGameValues(game):
    game.initMap() # also initialize generation_threshold and square_size
    game.initTerrain()
    
    game.worms = []
    game.current_worm_id = 0
    game.worm_has_fired = False
    game.objects = []
    game.rangedWeapons = [Item.Grenade]
    
    game.inventory = Inventory()
    game.inventoryOpenState = InventoryState.Closed
    
    game.clock = pg.time.Clock()
    game.state = GameState.INTERACTIVE
    game.turnTimer = 0



def mainloop(screen, game):
    global TERRAIN_IMG
    global PG_TERRAIN_IMG
    
    xmax, ymax = pg.display.get_surface().get_size()
    Settings.XMAX = xmax
    Settings.YMAX = ymax
    
    initGameValues(game)
    
    TERRAIN_IMG = Image.open('../img/terrain4.jpg')
    TERRAIN_IMG = TERRAIN_IMG.resize((xmax, ymax))
    # pg.transform.scale(TERRAIN_IMG, (xmax, ymax))
    
    PG_TERRAIN_IMG = pg.Surface((xmax, ymax), pg.SRCALPHA)
    for polygon in game.terrain.polygons:
        if len(polygon) > 2:
            # pg.draw.polygon(screen, (rd.randrange(255), rd.randrange(255), rd.randrange(255)), polygon)
            # pg.draw.polygon(screen, (200, 150, 50), polygon)
            
            # creating the mask
            mask = Image.new('RGBA', TERRAIN_IMG.size)
            d = ImageDraw.Draw(mask)
            d.polygon(polygon, fill='#000')
    
            out = Image.new('RGBA', TERRAIN_IMG.size)
            out.paste(TERRAIN_IMG, (0,0), mask)
            image_data = out.tobytes()
            image_dimensions = out.size
            pygame_surface = pg.image.fromstring(image_data, image_dimensions, 'RGBA')
            pygame_surface = pygame_surface.convert_alpha()
            PG_TERRAIN_IMG.blit(pygame_surface, (0,0))
    
    
    if Settings.NUMBEROFPLAYERS < 2:
        exit()
    for i in range(Settings.NUMBEROFPLAYERS):
        w = Worm((i + 1) * 50, ymax - Worm.radius - 1)
        game.worms.append(w)

    running = True
    while running:
        events = pg.event.get()
        pressed = pg.key.get_pressed()

        if game.state == GameState.INTERACTIVE:
            for event in events:
                # stops the program when closing
                if event.type == pg.QUIT:
                    running = False
                    
                if event.type == pg.KEYDOWN:
                    # stops the program on clicking the escape button
                    if event.key == pg.K_ESCAPE:
                        running = False
                    
                    if game.inventoryOpenState == InventoryState.Closed:
                        if event.key == pg.K_SPACE:
                            game.worms[game.current_worm_id].jump()
                        elif event.key == pg.K_RSHIFT and not game.worm_has_fired:
                            game.inventoryOpenState = InventoryState.Opened
                    else:
                        if event.key == pg.K_RSHIFT:
                            game.inventory.changeSelectedItem()
                       
                if event.type == pg.KEYUP and game.inventoryOpenState == InventoryState.Opened:
                    if event.key == pg.K_SPACE:
                        game.inventory.triggerCurrentItem(game.worms[game.current_worm_id], game.objects)
                        game.state = GameState.ANIMATION # TODO : seulement pour les weapons ou les rangedWeapons?
                        game.worm_has_fired = True
            
            if game.inventoryOpenState == InventoryState.Closed:
                if pressed[pg.K_q]:
                    game.worms[game.current_worm_id].moveLeft()
                elif pressed[pg.K_d]:
                    game.worms[game.current_worm_id].moveRight()
                    
            elif game.inventory.currentItem() in game.rangedWeapons:
                if pressed[pg.K_q]:
                    game.worms[game.current_worm_id].aimLeft()
                    # print(game.worms[game.current_worm_id].aimAngle)

                if pressed[pg.K_d]:
                    game.worms[game.current_worm_id].aimRight()
                    # print(game.worms[game.current_worm_id].aimAngle)

                if pressed[pg.K_SPACE]:
                    game.worms[game.current_worm_id].charge()


        for i in range(len(game.worms)):
            game.worms[i].refreshState()

        for obj in game.objects:
            if isinstance(obj, Grenade):
                if pg.time.get_ticks() - obj.creation_tick > 5000:
                    # TODO: boom animation + appliquer dégâts au terrain
                    Explosion.draw_explosion(screen, (obj.x, obj.y))
                    obj.explode(game.worms)
                    game.objects.remove(obj)
                    game.state = GameState.INTERACTIVE

        for w in game.worms:
            if w.hp <= 0:
                game.worms.remove(w)

        # TODO: si plus qu'un seul wormms, lui attribuer la victoire
        if len(game.worms) <= 1:
            print("Fin de la partie")
            running = False

        draw(screen, game)

        game.clock.tick(40)
        game.turnTimer += 40
        if (game.turnTimer >= Settings.NUMBERMILLISECONDSTURN) or game.worm_has_fired:
            game.worms[game.current_worm_id].powerCharge = 0
            game.worms[game.current_worm_id].aimAngle = -90
            game.current_worm_id = (game.current_worm_id + 1) % len(game.worms)
            print("current_worm_id : {}".format(game.current_worm_id))
            game.turnTimer = 0
            game.inventoryOpenState = InventoryState.Closed
            game.worm_has_fired = False
            print("Nouveau tour")

    print("Fermeture du programme")
    pg.quit()
    quit()


def screenInit():
    print("\nProgram initialisation...")

    pg.init()
    screen = pg.display.set_mode((900, 600), pg.RESIZABLE)
    screen.fill(Settings.BACKGROUNDCOLOR)
    pg.display.flip()

    return screen


if __name__ == "__main__":
    # the script runs in its own directory instead of the location where it was launched
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
    
    screen = screenInit()
    game = Model()
    mainloop(screen, game)
