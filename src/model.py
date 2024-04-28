from enum import Enum
from map2D import *
from terrain import *
from settings import *
from inventory import *
from worm import *

class GameState(Enum):
    INTERACTIVE = 1
    ANIMATION = 2

class InventoryState(Enum):
    Closed = 0
    Opened = 1

class Model:
    
    def __init__(self, clock):
        self.view = None
        
        self.map = None
        self.generation_threshold = None
        self.square_size = None
        self.terrain = None
        
        self.worms = []
        self.current_worm_id = 0
        self.worm_has_fired = False
        self.objects = []
        self.rangedWeapons = [Item.Grenade, Item.Bazooka]
        
        self.inventory = Inventory()
        self.inventoryState = InventoryState.Closed
        
        self.clock = clock
        self.state = GameState.INTERACTIVE
        self.turnTimer = 0
        
        self.initMap() # also initialize generation_threshold and square_size
        self.initTerrain()
    
        # TODO : plusieurs worms appartenant à un joueur et gerer le chgt de tour
        for i in range(Settings.NUMBEROFPLAYERS * Settings.WORMSBYPLAYER):
            w = Worm((i + 1) * 200, 100)
            self.worms.append(w)
    
    def setView(self, view):
        self.view = view
    
    def initMapTest(self):
        self.map = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
                    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                    [0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0],
                    [0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0],
                    [0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0],
                    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                    ]
        self.generation_threshold = 0.5
        self.square_size = 20
    
    def initMap(self):
        w = Settings.XMAX // Settings.MAP_SQUARE_SIZE
        h = Settings.YMAX // Settings.MAP_SQUARE_SIZE
        self.map = Map2D(w, h, Settings.MAP_COEF_MIN, Settings.MAP_COEF_MAX).getCoefsFormatted()
        self.generation_threshold = Settings.MAP_THRESHOLD
        self.square_size = Settings.MAP_SQUARE_SIZE
    
    def initTerrain(self):
        self.terrain = Terrain(self.map, self.square_size, self.generation_threshold)
    
    def hasInventoryOpened(self):
        return (self.inventoryState == InventoryState.Opened)
    
    def getCurrentWorm(self):
        return self.worms[self.current_worm_id]