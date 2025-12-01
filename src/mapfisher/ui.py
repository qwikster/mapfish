import sys
import shutil
import json
from mapfisher.input import read_key
from mapfisher.geocode import geocode_location, get_current_suggestions, trigger_async_search

CONFIG_FILE = "config.json"

BOX_WIDTH = 64
BOX_HEIGHT = 12

COLOR_RESET = "\x1b[0m"
COLOR_HIGHLIGHT = "\x1b[47;30m"
COLOR_SELECTED = "\x1b[42;30m"
COLOR_PROMPT = "\x1b[34m"


def clear():
    sys.stdout.write("\x1b[2J\x1b[H")
    sys.stdout.flush()

def get_terminal_size():
    return shutil.get_terminal_size((80, 24))

class SettingsUI:
    def __init__(self, config):
        self.options = [
            {"name": "precip", "label": "Distance Units"   , "states": ["mm", "inch"], "value": config["units_precip"]},
            {"name": "temp"  , "label": "Temperature Units", "states": ["°C", "°F"  ], "value": config["units_temp"]},
            {"name": "search", "label": "Search Locations" , "states": None          , "value": None},
            {"name": "quit"  , "label": "Quit"             , "states": None          , "value": None},
        ]
        self.current_option = 0
        self.search_mode = False
        self.search_input = ""
        self.suggestions = []
        self.selected_sugg = 0
        self.config = config
    
    def draw_ui(self):
        clear()
        lines = [
            "Settings",
            ""
        ]
        
        for i, opt in enumerate(self.options[:]):
            highlight = COLOR_HIGHLIGHT if i == self.current_option and not self.search_mode else ""
            if opt["states"]:
                state_idx = opt["states"].index(opt["value"])
                states_str = " | ".join(
                    COLOR_SELECTED + s + COLOR_RESET if j == state_idx else s
                    for j, s in enumerate(opt["states"])
                )
                lines.append(f"{highlight}  {opt["label"]}: {states_str}{COLOR_RESET}")
            else:
                lines.append(f"{highlight}  {opt["label"]}{COLOR_RESET}")
        
        draw_box(lines)
        
        if self.search_mode:
            term_w, term_h = get_terminal_size()
            box_x = (term_w - BOX_WIDTH) // 2
            box_y = (term_h - BOX_HEIGHT) // 2
            
            prompt_y = box_y + 7
            sugg_start_y = prompt_y + 2
            
            prompt = f"{COLOR_PROMPT}Coordinates >... {self.search_input}{COLOR_RESET}"
            sys.stdout.write(f"\x1b[{prompt_y};{box_x + 3}H{prompt.ljust(BOX_WIDTH - 6)}")
            
            current_suggs = get_current_suggestions()
            for i in range(5):
                y = sugg_start_y + i
                sys.stdout.write(f"\x1b[{y};{box_x + 3}H{' ' * (BOX_WIDTH - 6)}")
                if i < len(current_suggs):
                    text = current_suggs[i][:BOX_WIDTH - 8]
                    hl = COLOR_SELECTED if i == self.selected_sugg else ""
                    sys.stdout.write(f"\x1b[{y};{box_x + 3}H  {hl}{text}{COLOR_RESET}")
                
            cursor_x = box_x + 3 + len("Coordinates >... ") + len(self.search_input)
            sys.stdout.write(f"\x1b[{prompt_y};{cursor_x}H")
            sys.stdout.flush()
                
    def run(self):
        self.draw_ui()
        
        while True:
            key = read_key()
            
            if not self.search_mode:
                # nav mode
                if key in ("w", "up"):
                    self.current_option = max(0, self.current_option - 1)
                elif key in ("s", "down"):
                    self.current_option = min(len(self.options) - 1, self.current_option + 1)
                elif key in ("a", "left"):
                    self.toggle_state(-1)
                elif key in ("d", "right"):
                    self.toggle_state(1)
                elif key == "enter":
                    if self.options[self.current_option]["name"] == "search":
                        self.search_mode = True
                    elif self.options[self.current_option]["name"] == "quit":
                        return "quit"
                
            else:
                # search mode
                if key == "esc":
                    self.search_mode  = False
                    self.search_input = ""
                    self.selected_sugg = 0
                elif key == "backspace":
                    self.search_input = self.search_input[:-1]
                    trigger_async_search(self.search_input)
                elif key == "up":
                    self.selected_sugg = max(0, self.selected_sugg - 1)
                elif key == "down":
                    current = get_current_suggestions()
                    self.selected_sugg = min(len(current) - 1, self.selected_sugg + 1)
                elif len(key) == 1 and (key.isprintable() or key in " °'\" "):
                    self.search_input += key
                    trigger_async_search(self.search_input)
                elif key == "enter":
                    final = (get_current_suggestions()[self.selected_sugg]
                             if get_current_suggestions() and self.selected_sugg < len(get_current_suggestions())
                             else self.search_input)
                    lat, lon = geocode_location(final)
                    if lat and lon:
                        self.search_mode = False
                        self.search_input = ""
                        self.selected_sugg = 0
                        return (lat, lon)
                    
            self.draw_ui()
    
    def toggle_state(self, direction):
        opt = self.options[self.current_option]
        if opt["states"]:
            idx = opt["states"].index(opt["value"])
            new_idx = (idx + direction) % len(opt["states"])
            opt["value"] = opt["states"][new_idx]
            self.config[opt["name"]] = opt["value"]
            save_config(self.config) # noqa - from MAIN.PY
        
def draw_box(lines):
    clear()
    term_width, term_height = get_terminal_size()
    start_x = (term_width - BOX_WIDTH) // 2
    start_y = (term_height - BOX_HEIGHT) // 2
    
    sys.stdout.write(f"\x1b[{start_y};{start_x}H")
    
    sys.stdout.write("╭" + "─" * (BOX_WIDTH - 2) + "╮\n")
    
    ln = 0
    for line in lines:
        ln += 1
        padded = line.center(BOX_WIDTH - 2)
        sys.stdout.write(f"\x1b[{start_y + ln};{start_x}H")
        sys.stdout.write("│" + padded + "│")
        
    for _ in range(BOX_HEIGHT - 2 - len(lines)):
        sys.stdout.write("│" + " " * (BOX_WIDTH - 2) + "│\n")
    
    sys.stdout.write("╰" + "─" * (BOX_WIDTH - 2) + "╯\n")
    
def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)
