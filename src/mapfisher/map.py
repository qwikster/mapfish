# Actual map rendering

import staticmaps # py-staticmaps
from img2unicode import FastGenericDualOptimizer, FastQuadDualOptimizer, HalfBlockDualOptimizer, Renderer
from PIL import ImageDraw
from io import BytesIO, StringIO
import sys
import os
import time

def textsize(self, text, font=None):
    bbox = self.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]
    
ImageDraw.ImageDraw.textsize = textsize

def render_map(lat, lon, zoom=14, width=640, height=360): # TODO: make dynamic/configurable later - Q/E keys?
    start_time = time.perf_counter()
    
    context = staticmaps.Context()
    context.set_tile_provider(staticmaps.tile_provider_ArcGISWorldImagery) # try other ones later this one definitely works
    center = staticmaps.create_latlng(lat, lon)
    
    context.set_center(center)
    context.set_zoom(zoom)
    setup_time = time.perf_counter()
    
    image = context.render_pillow(width, height)
    maprend_time = time.perf_counter()
    
    fd = sys.stdout.fileno()
    columns, rows = os.get_terminal_size(fd)
    max_w = columns - 2
    max_h = int(rows * 0.5) - 5
    
    optimizer = FastGenericDualOptimizer("block") # also consider changing render types
    renderer = Renderer(default_optimizer = optimizer, max_w = max_w, max_h = max_h) # will need to ebe changed for gamma variants
    setrend_time = time.perf_counter()
    
    out = StringIO()
    renderer.render_terminal(image, out, optimizer = optimizer)
    final_time = time.perf_counter()
    
    data = out.getvalue()
    print("\x1b[H\x1b[2J")
    print(data)
    
    print("lat/long: ", lat, lon, "\nzoom: ", zoom, "\nsize: ", width, height)
    print("Setup:       ", setup_time - start_time)
    print("Map render:  ", maprend_time - setup_time)
    print("Rend setup:  ", setrend_time - maprend_time)
    print("img2unicode: ", final_time - setrend_time)
    print("Elapsed:     ", final_time - start_time)
    
    return data