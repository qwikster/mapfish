import sys
import shutil
import re
from mapfisher.input import read_key
from mapfisher.map import render_map
from mapfisher.ui import clear, get_terminal_size
from mapfisher.weather import fetch_weather, WEATHER_CODES

def display_width(s):
    # regex by ai
    s = re.sub(r'\x1b\[[0-9;]*m', '', s)
    return len(s)

def draw_weather_box(start_y, start_x, lines, box_w): # REVISE
    pass

class MapViewUI:
    def __init__(self, lat, lon, config):
        self.lat = lat
        self.lon = lon
        self.config = config
        self.zoom = 14
        self.map_data = None
        self.weather_data = fetch_weather(self.lat, self.lon, self.config)
        
    def show_loading(self):
        clear()
        term_w, term_h = get_terminal_size()
        msg = "Loading... ☺"
        x = (term_w - len(msg)) // 2
        y = term_h // 2
        sys.stdout.write(f"\x1b[{y};{x}H{msg}")
        sys.stdout.flush()
        
    def draw_ui(self):
        clear()
        sys.stdout.write(self.map_data + "\n")
        term_w, term_h = get_terminal_size()
        
        # weather box
        box_x = (term_w - 38) // 2
        box_y = 2
        sys.stdout.write(f"\x1b[{box_y};{box_x}H ╭──────────────────────────────────────╮")
        
        # controls
        controls = "\x1b[38;5;86m< \x1b[32m[+/-]\x1b[38;5;86m zoom | \x1b[32m[r]\x1b[38;5;86meload | \x1b[32m[esc/q]\x1b[38;5;86m back >"
        controls_visw = display_width(controls)
        controls_x = term_w - controls_visw - 4
        controls_y = term_h - 1
        sys.stdout.write(f"\x1b[{controls_y};{controls_x}H{controls}")
        sys.stdout.flush()
        
    def run(self):
        self.refresh_map()
        while True:
            key = read_key()
            if key in ("+", "="):
                self.zoom = min(18, self.zoom + 1)
                self.refresh_map()
            elif key == "-":
                self.zoom = max(1, self.zoom - 1)
                self.refresh_map()
            elif key == "r":
                self.weather_data = fetch_weather(self.lat, self.lon, self.config)
                self.draw_ui()
            elif key in ("esc", "q"):
                return
            
    def refresh_map(self):
        self.show_loading()
        self.map_data = render_map(self.lat, self.lon, self.zoom)
        self.draw_ui()