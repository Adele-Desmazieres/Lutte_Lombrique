import pygame as pg
from PIL import Image, ImageDraw
from settings import *
import random as rd

class View:
    
    def __init__(self, screen, game):
        self.screen = screen
        self.font_big = pg.font.Font(Settings.FONTNAME, Settings.FONTSIZEBIG)
        self.font_small = pg.font.Font(Settings.FONTNAME, Settings.FONTSIZESMALL)
        
        self.terrain_img = pg.image.load(Settings.TERRAIN_IMG_PATH)
        self.terrain_img = pg.transform.flip(self.terrain_img, False, True)
        self.terrain_img = pg.transform.scale(self.terrain_img, (Settings.XMAX, Settings.YMAX))
        self.terrain_img.fill((180, 180, 100), special_flags=pg.BLEND_RGB_MULT)
        self.terrain_img.fill((20, 20, 5), special_flags=pg.BLEND_RGB_ADD)
        self.terrain_img.fill((rd.randrange(50), rd.randrange(1), rd.randrange(50)), special_flags=pg.BLEND_RGB_ADD)
        size = self.terrain_img.get_size()
        string_img = pg.image.tobytes(self.terrain_img, 'RGBA')
        self.terrain_img = Image.frombytes('RGBA', size, string_img)

        # self.terrain_img = Image.open(Settings.TERRAIN_IMG_PATH)
        # self.terrain_img = self.terrain_img.resize((Settings.XMAX, Settings.YMAX))
        
        self.pg_terrain_img = None
        self.pg_terrain_img = self.update_terrain_img(game)
        
        self.pg_terrain_img_initial = self.pg_terrain_img.copy()
        self.pg_terrain_img_initial.fill((100, 100, 100), special_flags=pg.BLEND_RGB_SUB)
        
        self.pg_sky_img = pg.image.load(Settings.SKY_IMG_PATH)
        self.pg_sky_img = pg.transform.scale(self.pg_sky_img, (Settings.XMAX, Settings.YMAX))
        self.pg_sky_img.fill((50, 90, 50, 0), special_flags=pg.BLEND_RGBA_MULT)
        
    
    def update_terrain_img(self, game):
        cropped_img = pg.Surface((Settings.XMAX, Settings.YMAX), pg.SRCALPHA)
        
        # Source éditée : https://stackoverflow.com/a/51537885
        # create the mask
        mask = Image.new('RGBA', self.terrain_img.size)
        d = ImageDraw.Draw(mask)
        
        # order polygons by size to draw the bigger first, and the smaller inside then
        pgs = game.terrain.polygons
        pgs = sorted(pgs, key=lambda x: x.length, reverse=True)
        
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
        return cropped_img

    def set_terrain_img(self, newimg):
        self.pg_terrain_img = newimg
    
    def draw(self, game):
        screen = self.screen
        
        # screen.fill(Settings.BACKGROUNDCOLOR)
        screen.blit(self.pg_sky_img, (0,0))
        screen.blit(self.pg_terrain_img_initial, (0,0))
        screen.blit(self.pg_terrain_img, (0,0))
    
        for s in game.terrain.surfaces:
            pg.draw.line(screen, (10, 10, 10), s.p, s.q, width=3)
    
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
    
    