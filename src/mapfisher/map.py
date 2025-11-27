# Actual map rendering

import staticmaps # py-staticmaps
from img2unicode import FastGenericDualOptimizer, FastQuadDualOptimizer, HalfBlockDualOptimizer, Renderer
from PIL import Image, ImageDraw
from io import BytesIO, StringIO
import sys
import shutil
import time

try:
    import tkinter
except ImportError:
    tkinter = None

def textsize(self, text, font=None):
    bbox = self.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]
    
ImageDraw.ImageDraw.textsize = textsize

def render_map(lat, lon, zoom=14, width=320, height=180, debug = False, fast = False): # TODO: make dynamic/configurable later - Q/E keys?
    start_time = time.perf_counter()
    
    context = staticmaps.Context()
    context.set_tile_provider(staticmaps.tile_provider_ArcGISWorldImagery) # make configurable
    center = staticmaps.create_latlng(lat, lon)
    
    context.set_center(center)
    context.set_zoom(zoom)
    setup_time = time.perf_counter()
    
    image = context.render_pillow(width, height)
    maprend_time = time.perf_counter()
    
    if tkinter:
        root = tkinter.Tk()
        upscale_width = root.winfo_screenwidth()
        upscale_height = root.winfo_screenheight()
        root.destroy()
    else:
        upscale_width, upscale_height = 1920, 1080 # assume size if it can't be found
    
    image = image.resize((upscale_width, upscale_height), resample = Image.LANCZOS)
    resize_time = time.perf_counter()

    columns, rows = shutil.get_terminal_size()
    max_w = columns - 2
    
    if fast:
        optimizer = FastQuadDualOptimizer()           # quad block chars
    else:
        optimizer = FastGenericDualOptimizer("block") # all block chars
    
    renderer = Renderer(default_optimizer = optimizer, max_w = max_w)
    setrend_time = time.perf_counter()
    
    out = StringIO()
    renderer.render_terminal(image, out, optimizer = optimizer)
    final_time = time.perf_counter()
    
    data = out.getvalue()
    lines = data.splitlines()
    data = "\n".join(lines[:-4]) # trim last 4 lines (provider watermark)
    
    # print("\x1b[H\x1b[2J")
    
    if debug:
        print("\x1b[H\x1b[2J")
        print(data)
        print("lat/long: ", lat, lon, "\nzoom: ", zoom, "\nsize: ", width, height)
        print("Setup:       ", setup_time - start_time)
        print("Map render:  ", maprend_time - setup_time)
        print("Resizing:    ", resize_time - maprend_time)
        print("Rend setup:  ", setrend_time - resize_time)
        print("img2unicode: ", final_time - setrend_time)
        print("Elapsed:     ", final_time - start_time)
    
    return data