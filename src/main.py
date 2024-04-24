#!/usr/bin/python3

import pygame as pg
import os
from settings import *
from terrain import *
from worm import *
from map2D import *
from weapon import *
from inventory import *
from explosion import *
from model import *
from view import *


def initGameValues(game):
    game.initMap() # also initialize generation_threshold and square_size
    game.initTerrain()
    
    game.worms = []
    game.current_worm_id = 0
    game.worm_has_fired = False
    game.objects = []
    game.rangedWeapons = [Item.Grenade, Item.Bazooka]
    
    game.inventory = Inventory()
    game.inventoryState = InventoryState.Closed
    
    game.clock = pg.time.Clock()
    game.state = GameState.INTERACTIVE
    game.turnTimer = 0
    
    if Settings.NUMBEROFPLAYERS < 2:
        exit()
    
    # TODO : plusieurs worms appartenant à un joueur et gerer le chgt de tour
    for i in range(Settings.NUMBEROFPLAYERS):
        w = Worm((i + 1) * 50, 100)#Settings.YMAX - Worm.radius - 1)
        game.worms.append(w)


def mainloop(game, view):
    
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
                    
                    if game.inventoryState == InventoryState.Closed:
                        if event.key == pg.K_SPACE:
                            game.worms[game.current_worm_id].jump()
                        elif event.key == pg.K_RSHIFT and not game.worm_has_fired:
                            game.inventoryState = InventoryState.Opened
                    else:
                        if event.key == pg.K_RSHIFT:
                            game.inventory.changeSelectedItem()
                       
                if event.type == pg.KEYUP and game.inventoryState == InventoryState.Opened:
                    if event.key == pg.K_SPACE:
                        game.inventory.triggerCurrentItem(game.worms[game.current_worm_id], game.objects)
                        game.state = GameState.ANIMATION # TODO : seulement pour les weapons ou les rangedWeapons?
                        game.worm_has_fired = True
            
            if game.inventoryState == InventoryState.Closed:
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
        
        # TODO : sortir ca du main si possible
        for obj in game.objects:
            if isinstance(obj, Grenade):
                if pg.time.get_ticks() - obj.creation_tick > 5000:
                    # TODO: boom animation + appliquer dégâts au terrain + force répulsion worms
                    Explosion.draw_explosion(screen, (obj.x, obj.y), obj.explosionRadius)
                    obj.explode(game.worms)
                    game.objects.remove(obj)
                    game.state = GameState.INTERACTIVE
            if isinstance(obj, Bazooka):
                if obj.collisionDetected: # TODO : if collision
                    Explosion.draw_explosion(screen, obj.collisionPoint, obj.explosionRadius)
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

        view.draw(game)

        game.clock.tick(40)
        game.turnTimer += 40
        if (game.turnTimer >= Settings.NUMBERMILLISECONDSTURN) or game.worm_has_fired:
            game.worms[game.current_worm_id].powerCharge = 0
            game.worms[game.current_worm_id].aimAngle = -90
            game.current_worm_id = (game.current_worm_id + 1) % len(game.worms)
            print("current_worm_id : {}".format(game.current_worm_id))
            game.turnTimer = 0
            game.inventoryState = InventoryState.Closed
            game.worm_has_fired = False
            print("Nouveau tour")

    print("Fermeture du programme")
    pg.quit()
    quit()


def screenInit():
    screen = pg.display.set_mode((Settings.XMAX, Settings.YMAX), pg.RESIZABLE)
    screen.fill(Settings.BACKGROUNDCOLOR)
    pg.display.flip()
    return screen


if __name__ == "__main__":
    print("\nProgram initialisation...")
    pg.init()
    
    # the script runs in its own directory instead of the location where it was launched
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
    
    # connects together model-view-controller
    game = Model()
    initGameValues(game)
    
    screen = screenInit()
    view = View(screen, game)
    
    mainloop(game, view)
