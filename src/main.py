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

	objects = []
	# TODO : crash si NUMBEROFPLAYERS < 2 ?
	for i in range(GameParameters.NUMBEROFPLAYERS):
		w = Worm((i + 1) * 50, (i + 1) * 50)
		w.deplacementVec.vx = 20
		objects.append(w)

	hasFired = False
	inventoryOpen = False
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
		for event in events:
			if event.type == pg.QUIT:
				running = False


		if not(inventoryOpen):
			if pressed[pg.K_q]:
				objects[currentId].moveLeft()
			elif pressed[pg.K_d]:
				objects[currentId].moveRight()
			elif pressed[pg.K_SPACE]:
				objects[currentId].jump()
			elif pressed[pg.K_RSHIFT]:
				inventoryOpen = True
		else:
			if pressed[pg.K_RSHIFT]:
				pass
				# TODO : change d'arme

		# TODO : if arm selected : on peut tirer avec, Q et D change la visée de l'arme

		# maj(objects)
		for i in range(GameParameters.NUMBEROFPLAYERS):
			objects[i].refreshState()

		draw(screen, objects)
		
		clock.tick(40)
		turnClock += 40
		if (turnClock >= GameParameters.NUMBERMILLISECONDSTURN) or hasFired:
			currentId = (currentId + 1) % GameParameters.NUMBEROFPLAYERS
			turnClock = 0
	
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
