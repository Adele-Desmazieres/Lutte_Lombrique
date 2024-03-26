import pygame as pg
from physical_objects import *
from game_parameters import *


def draw(screen, objects):
	screen.fill(GameParameters.BACKGROUNDCOLOR)
	
	for o in objects:
		o.moveFree()
		pg.draw.circle(screen, GameParameters.WORMCOLOR, (o.x, o.y), o.radius)
	
	pg.display.flip()




def mainloop(screen):
	clock = pg.time.Clock()

	w1 = Worm(50, 50)
	w1.deplacementVec.vx = 30
	w2 = Worm(100, 200)
	w2.deplacementVec.vx = 10
	objects = [w1, w2]
	running = True
	
	while running:
		xmax, ymax = pg.display.get_surface().get_size()
		GameParameters.XMAX = xmax
		GameParameters.YMAX = ymax
		events = pg.event.get()
		
		# stops the program when closing
		for event in events:
			if event.type == pg.QUIT :
				running = False 
		
		# maj(objects)
		draw(screen, objects)
		
		clock.tick(40)
	
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
