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
        self.rangedWeapons = [Item.Grenade]
        
        self.inventory = Inventory()
        self.inventoryState = InventoryState.Closed
        
        self.clock = clock
        self.state = GameState.INTERACTIVE
        self.turnTimer = 0
        
        self.initMap() # also initialize generation_threshold and square_size
        self.initTerrain()
    
        # TODO : plusieurs worms appartenant à un joueur et gerer le chgt de tour
        for i in range(Settings.NUMBEROFPLAYERS):
            w = Worm((i + 1) * 50, Settings.YMAX - Worm.radius - 1)
            self.worms.append(w)
    
    def setView(self, view):
        self.view = view
    
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