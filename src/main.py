import pygame as pg
from physical_objects import *
from game_parameters import *


class State(Enum):
    Moving = 0
    InventoryOpen = 1

def draw(screen, worms, objects, inventoryOpen, inventory):
    screen.fill(GameParameters.BACKGROUNDCOLOR)

    for w in worms:
        w.moveFree()
        w.draw(screen)

    for o in objects:
        print("ntm")
        o.moveFree()
        o.draw(screen)

    if (inventoryOpen):
        inventory.draw(screen)


    pg.display.flip()


def mainloop(screen):
    clock = pg.time.Clock()

    worms = []
    objects = []
    inventory = Inventory()
    maxX, maxY = pg.display.get_surface().get_size()
    # TODO : crash si NUMBEROFPLAYERS < 2 ?
    for i in range(GameParameters.NUMBEROFPLAYERS):
        w = Worm((i + 1) * 50, maxY - Worm.radius - 1)
        #w.deplacementVec.vx = 20
        worms.append(w)

    hasFired = False
    hasChanged = False
    currentState = State.Moving
    currentId = 0
    turnClock = 0

    running = True

    while running:
        xmax, ymax = pg.display.get_surface().get_size()
        GameParameters.XMAX = xmax
        GameParameters.YMAX = ymax
        events = pg.event.get()
        pressed = pg.key.get_pressed()

        # stops the program when closing
        for event in events: # TODO : KEYUP du space : on tire, pendant le keypressed, on charge, modifier ce qu'il y a à modifier
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
                    elif event.key == pg.K_SPACE: # TODO : weapon = nouvel objet | tool = pas d'objet créé
                        inventory.triggerCurrentItem(worms[currentId], objects)

        if currentState == State.Moving:
            if pressed[pg.K_q]:
                worms[currentId].moveLeft()
            elif pressed[pg.K_d]:
                worms[currentId].moveRight()
        else:
            # todo : afficher arme
            if pressed[pg.K_q]:
                pass # TODO : viser vers la gauche
            elif pressed[pg.K_d]:
                pass  # TODO : viser vers la droite


        for i in range(GameParameters.NUMBEROFPLAYERS):
            worms[i].refreshState()

        draw(screen, worms, objects, currentState == State.InventoryOpen, inventory)

        clock.tick(40)
        turnClock += 40
        if (turnClock >= GameParameters.NUMBERMILLISECONDSTURN) or hasFired:
            currentId = (currentId + 1) % GameParameters.NUMBEROFPLAYERS
            turnClock = 0
            currentState = State.Moving
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
    screen = screenInit()
    mainloop(screen)
