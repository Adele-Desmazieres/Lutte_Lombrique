import random as rd

class Settings:
	
	GRAVITY = 0.18
	FRICTION = 0.999 # more like fluidity, used to multiply a vector by this to slow it down
	BOUNCINGABSORPTION = 0.6
	MAX_POWER_CHARGE = 100
	
	XMIN = 0
	XMAX = 900
	YMIN = 0
	YMAX = 600
	MAP_SQUARE_SIZE = 10 # en pixel
	MAP_COEF_MIN = 0
	MAP_COEF_MAX = 10
	MAP_THRESHOLD = 5 # seuil entre le terrain si coef supérieur, et l'air si coef inférieur
	
	TERRAIN_IMG_PATH = '../img/terrain' + str(rd.randrange(1, 5)) + '.jpg'
	# TERRAIN_IMG_PATH = '../img/terrain6.jpg'
	SKY_IMG_PATH = '../img/sky3.jpg'
	# SKY_IMG_PATH = TERRAIN_IMG_PATH
	WORM_IMG_PATH = "../img/worm.png"
	BACKGROUNDCOLOR = (30, 30, 100)
	WORMCOLOR = (230, 143, 124)
	FONTNAME = "freesansbold.ttf"
	FONTSIZEBIG = 20
	FONTSIZESMALL = 10
	
	NUMBEROFPLAYERS = 2
	WORMSBYPLAYER = 2
	NUMBERMILLISECONDSTURN = 30000
	JUMPPOWER = 4

