from enum import Enum
from map2D import *
from terrain import *
from settings import *

class GameState(Enum):
    INTERACTIVE = 1
    ANIMATION = 2

class InventoryState(Enum):
    Closed = 0
    Opened = 1

class Model:
    
    def __init__(self):
        self.map = None
        self.generation_threshold = None
        self.square_size = None
        self.terrain = None
        
        self.worms = None
        self.current_worm_id = None
        self.worm_has_fired = None
        self.objects = None
        self.rangedWeapons = None
        
        self.inventory = None
        self.inventoryState = None
        
        self.clock = None
        self.state = None
        self.turnTimer = None
        
        # self.currentState = None
    
    def initMap(self):
        # map = [[0, 0, 0, 0, 0, 0, 0], 
        #        [0, 1, 1, 1, 0, 0, 0],
        #        [0, 1, 1, 1, 1, 0, 0],
        #        [0, 1, 1, 1, 1, 1, 0],
        #        [0, 0, 0, 0, 0, 0, 0]
        #        ]
        # generation_threshold = 0.5
        # square_size = 60
    
        self.map = Map2D(90, 60, 0, 10).getCoefsFormatted()
        self.generation_threshold = 5
        self.square_size = min(Settings.YMAX/(len(self.map[0])-1), Settings.XMAX/(len(self.map)-1))
    
    def initTerrain(self):
        self.terrain = Terrain(self.map, self.square_size, self.generation_threshold)
    
    def hasInventoryOpened(self):
        return (self.inventoryState == InventoryState.Opened)