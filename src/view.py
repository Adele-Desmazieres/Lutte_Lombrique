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
        
        self.target_img = pg.image.load(Settings.TARGET_IMG_PATH)
        self.target_img = pg.transform.scale(self.target_img, (20, 20))
        
    
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
            w.draw(self, screen, game.isCurrentWorm(w))
    
        for o in game.objects:
            o.draw(screen)
    
        # affichage de l'eau
        maxHeight = Settings.YMAX
        waterHeight = maxHeight * (game.numberOfTurns / Settings.MAX_TURNS_NUMBER)  # Hauteur du filtre basée sur le nombre de tours
        waterSurface = pg.Surface((screen.get_width(), maxHeight))
        waterSurface.set_alpha(128)  # Opacité
        waterSurface.fill((0, 0, 255))
        screen.blit(waterSurface, (0, maxHeight - waterHeight),
                    area=(0, maxHeight - waterHeight, screen.get_width(), waterHeight))
        
        if (game.hasInventoryOpened()):
            game.inventory.draw(screen)
            if game.inventory.currentItem() in game.ranged:
                game.getCurrentWorm().draw_line_of_sight(screen)
    
        if game.inventory.currentItem() in game.ranged:
            game.worms[game.current_worm_id].draw_aiming_cursor(screen)
        
        # affiche le curseur
        if (game.hasInventoryOpened()) and game.inventory.currentItem() not in game.ranged: 
            self.draw_custom_cursor(self.target_img)
        else:
            pg.mouse.set_visible(True)
            
        
        # affiche le timer du tour
        t = (Settings.NUMBERMILLISECONDSTURN - game.turnTimer) // 1000
        text = self.font_big.render(str(t), True, (250, 250, 250))
        textRect = text.get_rect() # create a rectangular object for the text surface object
        textRect.topleft = (10, 10) # set the position of the rectangular object
        screen.blit(text, textRect)
            
        pg.display.flip()
    
    # source : https://github.com/Mekire/pygame-image-outline/blob/master/outline.py
    def draw_outline(self, img, coords, color):
        outline = pg.mask.from_surface(img).outline()
        outline_image = pg.Surface(img.get_size()).convert_alpha()
        outline_image.fill((0,0,0,0))
        for point in outline:
            outline_image.set_at(point, color)
        x,y = coords
        self.screen.blit(outline_image, (x+1, y  ))
        self.screen.blit(outline_image, (x  , y+1))
        self.screen.blit(outline_image, (x-1, y  ))
        self.screen.blit(outline_image, (x  , y-1))
    
    # source : https://stackoverflow.com/a/63409603
    def draw_custom_cursor(self, cursor_img):
        pg.mouse.set_visible(False)
        cursor_img_rect = cursor_img.get_rect()
        pos = pg.mouse.get_pos()
        cursor_img_rect.center = pos # update position 
        self.draw_outline(cursor_img, cursor_img_rect.topleft, (255, 0, 0))
        self.screen.blit(cursor_img, cursor_img_rect) # draw the cursor
        