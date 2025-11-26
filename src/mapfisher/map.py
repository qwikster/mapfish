# Actual map rendering

import staticmaps # py-staticmaps
from img2unicode import FastGenericDualOptimizer, Renderer
from PIL import ImageDraw
from io import BytesIO, StringIO
import sys
import time

def textsize(self, text, font=None):
    bbox = self.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]
    
ImageDraw.ImageDraw.textsize = textsize

def render_map(lat, lon, zoom=16, width=800, height=400): # TODO: make dynamic/configurable later - Q/E keys?
    start_time = time.perf_counter()
    
    context = staticmaps.Context()
    ctx_time = time.perf_counter()
    
    context.set_tile_provider(staticmaps.tile_provider_ArcGISWorldImagery) # try other ones later this one definitely works
    center = staticmaps.create_latlng(lat, lon)
    setting_time = time.perf_counter()
    
    context.set_center(center)
    context.set_zoom(zoom)
    zoom_time = time.perf_counter()
    
    image = context.render_pillow(width, height)
    maprend_time = time.perf_counter()
    
    optimizer = FastGenericDualOptimizer("block") # also consider changing render types
    renderer = Renderer(default_optimizer = optimizer, max_h = 120, max_w = 240) # will need to ebe changed for gamma variants
    
    renderer.render_terminal(image, sys.stdout, optimizer = optimizer)