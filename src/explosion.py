import random as rd
import pygame as pg

EXPLOSIONCOLORS = [(255, 69, 0), (255, 150, 0), (255, 215, 0)]

class Explosion:
    
    def __init__(self):
        pass
    
    def draw_explosion(screen, position, max_radius):
        num_circles = 10
        clock = pg.time.Clock()
    
        pg.draw.circle(screen, rd.choice(EXPLOSIONCOLORS), position, max_radius)
    
        for i in range(num_circles):
            radius = rd.randint(5, max_radius)
            color = rd.choice(EXPLOSIONCOLORS)
            pg.draw.circle(screen, color, position, radius)
            max_radius -= 5
            clock.tick(40)
            pg.display.flip() # TODO : pas très propre ? à changer ?
