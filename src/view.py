import pygame as pg
from PIL import Image, ImageDraw
from settings import *

class View:
    
    def __init__(self, screen, game):
        self.screen = screen
        
        self.terrain_img = Image.open(Settings.TERRAIN_IMG_PATH)
        self.terrain_img = self.terrain_img.resize((Settings.XMAX, Settings.YMAX))
        
        self.pg_terrain_img = None
        self.update_terrain_img(game)
    
    def update_terrain_img(self, game):
        cropped_img = pg.Surface((Settings.XMAX, Settings.YMAX), pg.SRCALPHA)
        
        for polygon in game.terrain.polygons:
            
            if len(polygon) <= 2:
                continue
            # pg.draw.polygon(screen, (rd.randrange(255), rd.randrange(255), rd.randrange(255)), polygon)
            # pg.draw.polygon(screen, (200, 150, 50), polygon)
            
            # create the mask
            mask = Image.new('RGBA', self.terrain_img.size)
            d = ImageDraw.Draw(mask)
            d.polygon(polygon, fill='#000')
            
            # cut out the form of the mask from the image terrain_img
            out = Image.new('RGBA', self.terrain_img.size)
            out.paste(self.terrain_img, (0,0), mask)
            out_data = out.tobytes()
            out_dimensions = out.size
            out_pygame_surface = pg.image.fromstring(out_data, out_dimensions, 'RGBA')
            
            # optimisation
            out_pygame_surface = out_pygame_surface.convert_alpha()
            
            # add this polygon to the final image
            cropped_img.blit(out_pygame_surface, (0,0))
                
        self.pg_terrain_img = cropped_img

    
    def draw(self, game):
        screen = self.screen
        
        screen.fill(Settings.BACKGROUNDCOLOR)
        screen.blit(self.pg_terrain_img, (0,0))
    
        for s in game.terrain.surfaces:
            pg.draw.line(screen, (200, 200, 200), s.p, s.q, width=3)
    
        for w in game.worms:
            w.moveFree(game.terrain)
            w.draw(screen)
    
        for o in game.objects:
            o.moveFree(game.terrain)
            o.draw(screen)
    
        if (game.hasInventoryOpened()):
            game.inventory.draw(screen)
    
        if game.inventory.currentItem() in game.rangedWeapons:
            game.worms[game.current_worm_id].draw_aiming_cursor(screen)
    
        pg.display.flip()
    
    