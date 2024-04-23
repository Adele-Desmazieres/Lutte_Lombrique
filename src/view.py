import pygame as pg
from PIL import Image, ImageDraw
from settings import *

class View:
    
    def __init__(self, screen, game):
        self.screen = screen
        self.font_big = pg.font.Font(Settings.FONTNAME, Settings.FONTSIZEBIG)
        self.font_small = pg.font.Font(Settings.FONTNAME, Settings.FONTSIZESMALL)
        
        self.terrain_img = Image.open(Settings.TERRAIN_IMG_PATH)
        self.terrain_img = self.terrain_img.resize((Settings.XMAX, Settings.YMAX))
        
        self.pg_terrain_img = None
        self.update_terrain_img(game)
    
    def update_terrain_img(self, game):
        cropped_img = pg.Surface((Settings.XMAX, Settings.YMAX), pg.SRCALPHA)
        
        # create the mask
        mask = Image.new('RGBA', self.terrain_img.size)
        d = ImageDraw.Draw(mask)
        
        # order polygon with terrain polygons first, then air polygons
        pgs = game.terrain.polygons
        pgs = sorted(pgs, key=lambda x: int(x.is_terrain), reverse=True)
        
        for polygon in pgs:
            
            if polygon.is_terrain:
                # fill the mask with black if the polygon is terrain
                d.polygon(polygon.points, fill=(0, 0, 0, 255))
            else:
                # otherwise fill the mask with transparent
                d.polygon(polygon.points, fill=(0, 0, 0, 0))
            
        out = Image.new('RGBA', self.terrain_img.size)
        
        # cut the form of the mask from the image terrain_img
        out.paste(self.terrain_img, (0,0), mask)
        out_data = out.tobytes('raw', 'RGBA')
        out_dimensions = out.size
        out_pygame_surface = pg.image.fromstring(out_data, out_dimensions, 'RGBA')
        
        # optimisation
        out_pygame_surface = out_pygame_surface.convert_alpha()
        
        # add this to the final pygame image
        cropped_img.blit(out_pygame_surface, (0,0))
                
        self.pg_terrain_img = cropped_img

    
    def draw(self, game):
        screen = self.screen
        
        screen.fill(Settings.BACKGROUNDCOLOR)
        screen.blit(self.pg_terrain_img, (0,0))
    
        for s in game.terrain.surfaces:
            pg.draw.line(screen, (00, 00, 00), s.p, s.q, width=2)
    
        for w in game.worms:
            w.moveFree()
            w.draw(screen, self)
    
        for o in game.objects:
            o.moveFree()
            o.draw(screen)
    
        if (game.hasInventoryOpened()):
            game.inventory.draw(screen)
            game.getCurrentWorm().draw_line_of_sight(screen)
    
        if game.inventory.currentItem() in game.rangedWeapons:
            game.worms[game.current_worm_id].draw_aiming_cursor(screen)
    
        pg.display.flip()
    
    