import sys
import shutil
from mapfisher.input import read_key
from mapfisher.geocode import suggest_locations

BOX_WIDTH = 60
BOX_HEIGHT = 12

COLOR_RESET = "\x1b[0m"
COLOR_HIGHLIGHT = "\x1b[47;30m"
COLOR_SELECTED = "\x1b[42;30m"
COLOR_PROMPT = "\x1b[34m"

def clear():
    sys.stdout.write("\x1b[2j\x1b[H")
    sys.stdout.flush()

def get_terminal_size():
    return shutil.get_terminal_size((80, 24))

class SettingsUI:
    def __init__(self, config):
        self.options = [
            {"name": "precip", "label": "Distance Units"   , "states": ["mm", "inch"], "value": config["units_precip"]},
            {"name": "temp"  , "label": "Temperature Units", "states": ["°C", "°F"  ], "value": config["units_temp"]},
            {"name": "search", "label": "Search Locations" , "states": None          , "value": None},
            {"name": "quit"  , "label": "Quit..."          , "states": None          , "value": None},
        ]
        self.current_option = 0
        self.search_mode = False
        self.search_input = ""
        self.suggestions = []
        self.selected_sugg = 0
    
    def draw_ui(self):
        clear()
        lines = [
            "Settings",
            ""
        ]
        
        for i, opt in enumerate(self.options[:-1]):
            highlight = COLOR_HIGHLIGHT if i == self.current_option else ""
            if opt["states"]:
                state_idx = opt["states"].index(opt["value"])
                states_str = " | ".join([COLOR_SELECTED + s + COLOR_RESET if j == state_idx else s for j, s in enumerate(opt["states"])])
                lines.append(f"{highlight}{opt["label"]}: {states_str}{COLOR_RESET}")
            else:
                lines.append(f"{highlight}{opt["label"]}{COLOR_RESET}")
        
        draw_box(lines)
        
        if self.search_mode:
            term_width, _ = get_terminal_size()
            prompt_y = BOX_HEIGHT // 2 + len(lines) // 2 + 1
            prompt_x = (term_width - BOX_WIDTH) // 2 + 1
            sys.stdout.write(f"\x1b[{prompt_y};{prompt_x}H")
            sys.stdout.write(f"{COLOR_PROMPT}>... {self.search_input}{COLOR_RESET}")
            
            for i, sugg in enumerate(self.suggestions):
                sugg_highlight = COLOR_SELECTED if i == self.selected_sugg else ""
                sys.stdout.write(f"\x1b[{prompt_y + i + 1};{prompt_x}H{sugg_highlight}{sugg[:BOX_WIDTH - 2]}{COLOR_RESET}")
            
            sys.stdout.flush()
                
    def run(self):
        self.draw_ui()
        
        while True:
            key = read_key()
    
    def toggle_state(self, direction):
        opt = self.options[self.current_option]
        
    def update_suggestions(self):
        self.suggestions = suggest_locations(self.search_input)
        self.selected_sugg = 0
        
def draw_box(lines):
    term_width, term_height = get_terminal_size()
    