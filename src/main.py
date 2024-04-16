import pygame as pg
from physical_objects import *
from game_parameters import *
from terrain import *
from map2D import *


MAP1 = [[0, 0, 0, 0, 0, 0, 0] 
	  ,[0, 1, 0, 0, 1, 0, 0] 
	  ,[0, 1, 1, 0, 1, 0, 0] 
	  ,[0, 1, 1, 1, 1, 0, 0] 
	  ,[0, 1, 1, 0, 1, 0, 0] 
	  ,[0, 0, 0, 1, 0, 0, 1]
	  ]
# inverse la map
MAP = [[MAP1[i][j] for i in range(len(MAP1))] for j in range(len(MAP1[0]))]
# ajoute des 0 autour de la map
MAP1 = [[0] + MAP[i] + [0] for i in range(len(MAP))]
MAP = [[0] * len(MAP1[0])] + MAP1 + [[0] * len(MAP1[0])]
# print(MAP)

def draw(screen, terrain, objects):
	screen.fill(GameParameters.BACKGROUNDCOLOR)
	
	# for i in range(len(MAP)-1):
	# 	for j in range(len(MAP[i])-1):
	# 		pg.draw.circle(screen, (50, 150, 50), (i*terrain.square_size, j*terrain.square_size), 3)
	
	for s in terrain.surfaces:
		pg.draw.line(screen, (250, 250, 250), s.p, s.q, width=3)
		m, n = s.normalVectorSegmentMiddle()
		pg.draw.line(screen, (250, 50, 50), m, n, width=1) 
		# pg.draw.circle(screen, (50, 150, 50), m, 3)
	
	for o in objects:
		o.moveFree()
		pg.draw.circle(screen, GameParameters.WORMCOLOR, (o.x, o.y), o.radius)
	
	pg.display.flip()




def mainloop(screen):
	clock = pg.time.Clock()
	
	xmax, ymax = pg.display.get_surface().get_size()
	GameParameters.XMAX = xmax
	GameParameters.YMAX = ymax
	
	map = Map2D(100, 100, 0, 10).getCoefsFormatted()
	generation_threshold = 5
	
	square_size = min(GameParameters.YMAX/(len(map[0])-1), GameParameters.XMAX/(len(map)-1))
	
	terrain = Terrain(map, square_size, generation_threshold)
	
	# w1 = Worm(50, 50)
	# w1.deplacementVec.vx = 30
	# w2 = Worm(100, 200)
	# w2.deplacementVec.vx = 10
	
	objects = []
	
	running = True
	
	while running:
		events = pg.event.get()
		
		# stops the program when closing
		for event in events:
			if event.type == pg.QUIT :
				running = False 
		
		# maj(objects)
		draw(screen, terrain, objects)
		
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
