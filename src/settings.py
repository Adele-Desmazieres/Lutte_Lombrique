import random as rd

class Settings:
	
	GRAVITY = 0.18
	FRICTION = 0.8 # more like fluidity, used to multiply a vector by this to slow it down
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
	SKY_IMG_PATH = '../img/sky3.jpg'
	WORM_IMG_PATH = '../img/worm.png'
	TARGET_IMG_PATH = '../img/target.png'
	HERE_IMG_PATH = '../img/here.png'
	
	BACKGROUNDCOLOR = (30, 30, 100)
	WORMCOLOR = (230, 143, 124)
	FONTNAME = "freesansbold.ttf"
	FONTSIZEBIG = 30
	FONTSIZESMALL = 12
	HPCOLORS = [(255, 10, 10), (10, 255, 10), (0, 100, 255), (200, 200, 0), (0, 200, 200), (200, 0, 200), (100, 100, 0), (200, 200, 200)]
	NUMBEROFPLAYERS = 2
	WORMSBYPLAYER = 10
	NUMBERMILLISECONDSTURN = 30000
	JUMPPOWER = 4
	MAX_TURNS_NUMBER = 100
