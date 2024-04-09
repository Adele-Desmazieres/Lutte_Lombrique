import pygame as pg
from physical_objects import *
from game_parameters import *
from terrain import *

MAP1 = [[0, 0, 0, 0, 0, 0, 0] 
      ,[0, 1, 0, 0, 1, 0, 0]
      ,[0, 1, 1, 0, 1, 0, 0]
      ,[0, 1, 1, 1, 1, 0, 0]
      ,[0, 1, 1, 0, 1, 0, 0]
      ,[0, 0, 0, 1, 0, 0, 1]
      ]

MAP = [[MAP1[j][i] for j in range(len(MAP1))] for i in range(len(MAP1[0]))]

class State(Enum):
    Moving = 0
    InventoryOpen = 1

def draw(screen, terrain, worms, objects, inventoryOpen, inventory):
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


    pg.display.flip()


def mainloop(screen):
    clock = pg.time.Clock()
    terrain = Terrain(MAP)
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
                        # todo : use et shot c'est au moment où on retire le doigt de la barre !
            if event.type == pg.KEYUP:
                if event.key == pg.K_SPACE: # TODO : weapon = nouvel objet | tool = pas d'objet créé
                    inventory.triggerCurrentItem(worms[currentId], objects)

        if currentState == State.Moving:
            if pressed[pg.K_q]:
                worms[currentId].moveLeft()
            elif pressed[pg.K_d]:
                worms[currentId].moveRight()
        else:
            if pressed[pg.K_q]:
                worms[currentId].aimAngle -= 0.5 # todo : mutateur avec un angle max/min
                print(worms[currentId].aimAngle)

            elif pressed[pg.K_d]:
                worms[currentId].aimAngle += 0.5 # todo : mutateur avec un angle max/min
                print(worms[currentId].aimAngle)

            elif pressed[pg.K_SPACE]:
                pass # todo : augmenter power


        for i in range(GameParameters.NUMBEROFPLAYERS):
            worms[i].refreshState()

        draw(screen, terrain, worms, objects, currentState == State.InventoryOpen, inventory)

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
