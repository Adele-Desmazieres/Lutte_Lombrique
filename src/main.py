

import pygame as pg
import random
import os
from physical_objects import *
from game_parameters import *
from terrain import *
from map2D import *



COLORS = [(255, 69, 0), (255, 150, 0), (255, 215, 0)]

class GameState(Enum):
    INTERACTIVE = 1
    ANIMATION = 2

class State(Enum):
    Moving = 0
    InventoryOpen = 1


def draw_explosion(screen, position):
    max_radius = 60
    num_circles = 10
    clock = pg.time.Clock()

    pg.draw.circle(screen, random.choice(COLORS), position, max_radius)

    for i in range(num_circles):
        radius = random.randint(5, max_radius)
        color = random.choice(COLORS)
        pg.draw.circle(screen, color, position, radius)
        max_radius -= 5
        clock.tick(40)
        pg.display.flip() # TODO : pas très propre ? à changer ?


def draw(screen, terrain, worms, objects, inventoryOpen, inventory, rangedWeapons, currentId):
    screen.fill(GameParameters.BACKGROUNDCOLOR)
	
    for s in terrain.surfaces:
        pg.draw.line(screen, (250, 250, 250), s.p, s.q, width=3)
        m, n = s.normalVectorSegmentMiddle()
        pg.draw.line(screen, (250, 50, 50), m, n, width=1)

    for w in worms:
        w.moveFree()
        w.draw(screen)

    for o in objects:
        o.moveFree()
        o.draw(screen)

    if (inventoryOpen):
        inventory.draw(screen)

    if inventory.currentItem() in rangedWeapons:
        worms[currentId].draw_aiming_cursor(screen)

    pg.display.flip()


def mainloop(screen):

    xmax, ymax = pg.display.get_surface().get_size()
    GameParameters.XMAX = xmax
    GameParameters.YMAX = ymax
    clock = pg.time.Clock()
    
    map = Map2D(100, 100, 0, 10).getCoefsFormatted()
    generation_threshold = 5
    square_size = min(GameParameters.YMAX/(len(map[0])-1), GameParameters.XMAX/(len(map)-1))
    terrain = Terrain(map, square_size, generation_threshold)
	
    state = GameState.INTERACTIVE
    worms = []
    objects = []
    rangedWeapons = [Item.Grenade]
    inventory = Inventory()
    maxX, maxY = pg.display.get_surface().get_size()
    if GameParameters.NUMBEROFPLAYERS < 2:
        exit()
    for i in range(GameParameters.NUMBEROFPLAYERS):
        w = Worm((i + 1) * 50, maxY - Worm.radius - 1)
        #w.deplacementVec.vx = 20
        worms.append(w)

    hasFired = False
    currentState = State.Moving
    currentId = 0
    turnClock = 0

    running = True

    while running:
        events = pg.event.get()
        pressed = pg.key.get_pressed()

        if state == GameState.INTERACTIVE:
            for event in events:
                # stops the program when closing
                if event.type == pg.QUIT:
                    running = False
                    
                if event.type == pg.KEYDOWN:
                    if currentState == State.Moving:
                        if event.key == pg.K_SPACE:
                            worms[currentId].jump()
                        elif event.key == pg.K_RSHIFT and not hasFired:
                            currentState = State.InventoryOpen
                    else:
                        if event.key == pg.K_RSHIFT:
                            inventory.changeSelectedItem()
                            
                if event.type == pg.KEYUP and currentState == State.InventoryOpen:
                    if event.key == pg.K_SPACE:
                        inventory.triggerCurrentItem(worms[currentId], objects)
                        state = GameState.ANIMATION # TODO : seulement pour les weapons ou les rangedWeapons?
                        hasFired = True

            if currentState == State.Moving:
                if pressed[pg.K_q]:
                    worms[currentId].moveLeft()
                elif pressed[pg.K_d]:
                    worms[currentId].moveRight()
                    
            elif inventory.currentItem() in rangedWeapons:
                if pressed[pg.K_q]:
                    worms[currentId].aimLeft()
                    print(worms[currentId].aimAngle)

                if pressed[pg.K_d]:
                    worms[currentId].aimRight()
                    print(worms[currentId].aimAngle)

                if pressed[pg.K_SPACE]:
                    worms[currentId].charge()


        for i in range(len(worms)):
            worms[i].refreshState()

        for obj in objects:
            if isinstance(obj, Grenade):
                if pg.time.get_ticks() - obj.creation_tick > 5000:
                    # TODO: boom animation + appliquer dégâts au terrain
                    draw_explosion(screen, (obj.x, obj.y))
                    obj.explode(worms)
                    state = GameState.INTERACTIVE
                    objects.remove(obj)

        for w in worms:
            if w.hp <= 0:
                worms.remove(w)

        if len(worms) <= 1:
            print("Fin de la partie")
            break
        
        # TODO: si plus qu'un seul wormms, lui attribuer la victoire

        draw(screen, terrain, worms, objects, currentState == State.InventoryOpen, inventory, rangedWeapons, currentId)

        clock.tick(40)
        turnClock += 40
        if (turnClock >= GameParameters.NUMBERMILLISECONDSTURN) or hasFired:
            worms[currentId].powerCharge = 0
            worms[currentId].aimAngle = -90
            currentId = (currentId + 1) % len(worms)
            print("currentId : {}".format(currentId))
            turnClock = 0
            currentState = State.Moving
            hasFired = False
            print("Nouveau tour")

    print("Fermeture du programme")
    pg.quit()
    quit()


def screenInit():
    print("\nProgram initialisation...")

    pg.init()
    screen = pg.display.set_mode((900, 600), pg.RESIZABLE)
    screen.fill(GameParameters.BACKGROUNDCOLOR)
    pg.display.flip()

    return screen


if __name__ == "__main__":
    # the script runs in its own directory instead of the location where it was launched
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)

    screen = screenInit()
    mainloop(screen)
