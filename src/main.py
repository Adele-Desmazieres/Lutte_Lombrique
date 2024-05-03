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

def show_end_game_screen(screen, winners):
    screen.fill(Settings.BACKGROUNDCOLOR)
    font = pg.font.Font(None, 36)

    title = font.render("Gagnant(s)", True, (255, 0, 0))
    screen.blit(title, (Settings.XMAX // 2 - title.get_width() // 2, 50))

    startY = 150
    for winner in winners:
        text = font.render(f"Joueur {winner}", True, Settings.HPCOLORS[winner])
        screen.blit(text, (Settings.XMAX // 2 - text.get_width() // 2, startY))
        startY += 40

    pg.display.flip()

    waiting = True
    while waiting:
        for event in pg.event.get():
            # stops the program when closing
            if event.type == pg.QUIT:
                waiting = False
                    
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                waiting = False
    
    pg.quit()
    quit()
    


def endTurn(game):
    game.worms[game.current_worm_id].powerCharge = 0
    game.current_worm_id = (game.current_worm_id + 1) % len(game.worms)
    print("current_worm_id : {}".format(game.current_worm_id))
    game.turnTimer = 0
    game.inventoryState = InventoryState.Closed
    game.worm_has_fired = False
    game.numberOfTurns += 1
    print("Nouveau tour")

def mainloop(game, view):
    
    running = True
    actualPlayers = [n for n in range(Settings.NUMBEROFPLAYERS)]
    deadPlayersThisTurn = []
    
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
                        elif event.key == pg.K_RSHIFT or event.key == pg.K_LSHIFT:
                            if not game.worm_has_fired:
                                game.inventoryState = InventoryState.Opened
                    else:
                        if event.key == pg.K_RSHIFT or event.key == pg.K_LSHIFT:
                            game.inventory.changeSelectedItem()
                        elif event.key == pg.K_BACKSPACE:
                            game.inventoryState = InventoryState.Closed
                       
                if event.type == pg.KEYUP and game.inventoryState == InventoryState.Opened:
                    if event.key == pg.K_SPACE:
                        if game.inventory.currentItem() == Item.Teleporter:
                            x, y = pg.mouse.get_pos()
                            objTp = Teleporter()
                            objTp.teleport(x, y, game.worms[game.current_worm_id])
                            game.worm_has_fired = True
                            game.worms[game.current_worm_id].stuckGround = False
                            game.worms[game.current_worm_id].updatePos(game.terrain)
                        else:
                            game.inventory.triggerCurrentItem(game.worms[game.current_worm_id], game.objects)
                            game.state = GameState.ANIMATION
                            game.worm_has_fired = True
            
            if game.inventoryState == InventoryState.Closed:
                if pressed[pg.K_q]:
                    game.worms[game.current_worm_id].moveLeft(game.terrain)
                elif pressed[pg.K_d]:
                    game.worms[game.current_worm_id].moveRight(game.terrain)
                    
            elif game.inventory.currentItem() in game.ranged:
                if pressed[pg.K_q]:
                    game.worms[game.current_worm_id].aimLeft()

                if pressed[pg.K_d]:
                    game.worms[game.current_worm_id].aimRight()

                if pressed[pg.K_SPACE]:
                    game.worms[game.current_worm_id].charge()
        
        # TODO : sortir ca du main (pas fait par manque de temps, mais devrait être dans weapon.py)
        for obj in game.objects:
            if isinstance(obj, Grenade):
                if pg.time.get_ticks() - obj.creation_tick > 3000:
                    Explosion.draw_explosion(screen, (obj.x, obj.y), obj.explosionRadius)
                    obj.explode(game, [(obj.x, obj.y)])
                    game.objects.remove(obj)
                    game.state = GameState.INTERACTIVE
            if isinstance(obj, Bazooka):
                if obj.collisionDetected:
                    Explosion.draw_explosion(screen, obj.collisionPoint, obj.explosionRadius)
                    obj.explode(game, [obj.collisionPoint])
                    game.objects.remove(obj)
                    game.state = GameState.INTERACTIVE
            if isinstance(obj, PneumaticDrill):
                if obj.collisionDetected:
                    # x, y = obj.collisionPoint
                    angle = obj.deplacementVec.getAngleRadians()
                    dx = obj.explosionRadius * math.cos(angle)
                    dy = obj.explosionRadius * math.sin(angle)
                    cX, cY = obj.collisionPoint
                    # cX, cY = (obj.x, obj.y)
                    centers = []
                    for i in range(PneumaticDrill.nbExplosions):
                    # centers = [(cX, cY),
                                # (cX + dx, cY + dy),
                                # (cX + 2 * dx, cY + 2 * dy)]
                        centers.append((cX + i * dx, cY + i * dy))
                    obj.explode(game, centers)
                    for center in obj.centers:
                        Explosion.draw_explosion(screen, center, obj.explosionRadius)

                    game.objects.remove(obj)
                    game.state = GameState.INTERACTIVE

        for w in game.worms:
            w.refreshState(game)
            playerIndex = w.playerIndex
            wormIndex = game.worms.index(w)
            if w.hp <= 0:
                game.worms.remove(w)
                if game.current_worm_id >= len(game.worms):
                    game.current_worm_id = 0

                if w.shouldExplode:
                    Explosion.draw_explosion(screen, (w.x, w.y), 30)
                    w.explode(game, [(w.x, w.y)])

                if len([w for w in game.worms if w.playerIndex == playerIndex]) == 0:
                    actualPlayers.remove(playerIndex)
                    deadPlayersThisTurn = [playerIndex]

        # TODO: si plus qu'un seul wormms, lui attribuer la victoire
        if len(game.worms) <= 1:
            winners = [player for player in actualPlayers if player not in deadPlayersThisTurn]
            if len(winners) == 0:
                winners = deadPlayersThisTurn
            if len(winners) > 1:
                print("Égalité ! Les joueurs gagnants sont : ")
                for player in winners:
                    print("Joueur {}".format(player))
            else:
                print("Victoire du joueur {}".format(winners[0]))

            print("Fin de la partie")
            running = False
            show_end_game_screen(screen, winners)
        
        for w in game.worms:
            w.updatePos(game.terrain)
            
        for o in game.objects:
            o.updatePos(game.terrain)

        view.draw(game)

        framerate = game.clock.tick(40)
        game.turnTimer += framerate
        if (game.turnTimer >= Settings.NUMBERMILLISECONDSTURN) or game.worm_has_fired:
            endTurn(game)
            deadPlayersThisTurn = []


    print("Fermeture du programme")
    pg.quit()
    quit()


def screenInit():
    screen = pg.display.set_mode((Settings.XMAX, Settings.YMAX), pg.RESIZABLE)
    pg.display.set_caption("Lutte Lombric")
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
    game = Model(pg.time.Clock())
    screen = screenInit()
    view = View(screen, game)
    game.setView(view)
    
    if Settings.NUMBEROFPLAYERS < 2:
        exit()
    
    mainloop(game, view)
