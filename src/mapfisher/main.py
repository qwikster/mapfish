# Main entry point
import sys
import readline
import json
import os
from mapfisher.ui import SettingsUI
from mapfisher.geocode import location_completer
from mapfisher.map import render_map

CONFIG_FILE = "config.json" # TODO: check if distributors break this

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {
        "units_precip": "mm",
        "units_temp": "°C",
        "last_location": None
    }

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)
        
def entry():
    config = load_config()
    
    # fallback
    readline.set_completer(location_completer)
    readline.parse_and_bind("tab: complete")
    
    ui = SettingsUI(config)
    
    while True:
        result = ui.run()
        if result == "quit":
            break
        elif result and isinstance(result, tuple):
            lat, lon = result
            config["last_location"] = {
                "lat": lat,
                "lon": lon
            }
            save_config(config)
            
            # TODO: weather parser go here
            render_map(lat, lon)

if __name__ == "__main__":
    entry()