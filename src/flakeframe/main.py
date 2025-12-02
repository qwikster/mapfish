# Main entry point
import json
import os
from flakeframe.ui import SettingsUI
from flakeframe.mapview import MapViewUI

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
    # readline.set_completer(location_completer)
    # readline.parse_and_bind("tab: complete")
    
    while True:
        ui = SettingsUI(config)
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
            mapview = MapViewUI(lat, lon, config)
            mapview.run()

if __name__ == "__main__":
    entry()