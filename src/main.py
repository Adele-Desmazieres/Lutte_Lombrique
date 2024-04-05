import pygame as pg
import math
from physical_objects import *
from game_parameters import *


class Item(Enum):
    PneumaticDrill = 0
    Grenade = 1

class State(Enum):
    Moving = 0
    InventoryOpen = 1

def draw(screen, objects, inventoryOpen, sprites, selectedItem):
    screen.fill(GameParameters.BACKGROUNDCOLOR)

    for o in objects:
        o.moveFree()
        pg.draw.circle(screen, GameParameters.WORMCOLOR, (o.x, o.y), o.radius)

    if (inventoryOpen):
        y = math.floor((32 * selectedItem) / 256)
        x = (32 * selectedItem) % 256
        portion_rect = pg.Rect(x, 32 * y, 32, 32) # (400, 400),
        image_portion = sprites.subsurface(portion_rect)
        maxX, maxY = pg.display.get_surface().get_size()
        scaled_image = pg.transform.scale(image_portion, (128, 128))
        screen.blit(scaled_image, (maxX - 128, maxY - 128))


    pg.display.flip()


def mainloop(screen):
    clock = pg.time.Clock()
    sprites = pg.image.load("worms.png")

    objects = []
    items = [Item.PneumaticDrill, Item.Grenade, Item.PneumaticDrill, Item.Grenade]
    selectedItem = 0
    maxX, maxY = pg.display.get_surface().get_size()
    # TODO : crash si NUMBEROFPLAYERS < 2 ?
    for i in range(GameParameters.NUMBEROFPLAYERS):
        w = Worm((i + 1) * 50, maxY - Worm.radius - 1)
        #w.deplacementVec.vx = 20
        objects.append(w)

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
                        objects[currentId].jump()
                    elif event.key == pg.K_RSHIFT and not hasFired:
                        currentState = State.InventoryOpen
                else:
                    if event.key == pg.K_RSHIFT:
                        selectedItem = (selectedItem + 1) % len(items)
                    elif event.key == pg.K_SPACE:
                        if isinstance(items[selectedItem], Weapon):
                            # TODO : faire un while pressed
                            items[selectedItem].shot(100) # TODO : remplacer 100 par le pourcentage de "charge", passer les coordonnées du worms en param
                        else:
                            items[selectedItem].use() # TODO : passer les coordonnées du worms en param

        if currentState == State.Moving:
            if pressed[pg.K_q]:
                objects[currentId].moveLeft()
            elif pressed[pg.K_d]:
                objects[currentId].moveRight()
        else:
            # todo : afficher arme
            if pressed[pg.K_q]:
                pass # TODO : viser vers la gauche
            elif pressed[pg.K_d]:
                pass  # TODO : viser vers la droite


        # maj(objects)
        for i in range(GameParameters.NUMBEROFPLAYERS):
            objects[i].refreshState()

        draw(screen, objects, currentState == State.InventoryOpen, sprites, selectedItem)

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
