import configparser
import os
import sys
from dataclasses import dataclass
from typing import List, Optional
from flakeframe.input import read_key
from flakeframe.ui import display_width, display_center, get_terminal_size, goto

@dataclass
class Asset:
    name: str
    r: int
    g: int
    b: int
    fg: Optional[bool]

@dataclass
class Theme:
    name: str
    author: str
    assets: List[Asset]

class ThemeHandler:
    def __init__(self, default_theme =
                    Theme(name = "default", author = "qwik", assets = [
                        Asset(name = "fore", r=255, g=255, b=255, fg=True), Asset(name = "back", r=16, g=16, b=16, fg=False)
                    ]
                )):
        
        self.storage = configparser.ConfigParser() # should never be actually read except when loading from
        self.default_theme = default_theme
        self.current: Theme = None
        self.themes: List[Theme] = []
            
    def save(self):
        # save to configfile format then write to disk
        if not hasattr(self, "themefile"):
            raise RuntimeError("Attempted to save themes before savefile was picked, use load_savefile(path) first.")
        
        for theme in self.themes:
            self.storage[theme.name] = {
                "name": theme.name,
                "author": theme.author,
            }
            for asset in theme.assets:
                self.storage[theme.name][asset.name] = f"{asset.r}, {asset.g}, {asset.b}, {str(asset.fg)}"
        
        with open(self.themefile, "w") as themefile:
            self.storage.write(themefile)
    
    def load(self):
        # load from configfile format to usable OOP
        if not hasattr(self, "themefile"):
            raise RuntimeError("Attempted to load themes before savefile was picked, use load_savefile(path) first (or probably instead).")

        self.storage = configparser.ConfigParser() # CLEAR
        self.storage.read(self.themefile)
        self.load_theme(self.storage["DEFAULT"]["current_theme"])
        
        for th in self.storage.sections():
            assetlist = []
            for i in self.storage[th]:
                if i not in ["name", "author", "current_theme"]:
                    data = self.storage[th][i].split(", ")
                    assetlist.append(Asset(name = i, r = data[0], g = data[1], b = data[2], fg = data[3]))
            
            self.themes.append(Theme(
                name = self.storage[th]["name"],
                author = self.storage[th]["author"],
                assets = assetlist
            ))
    
    def new_theme(self, theme):
        self.themes.append(theme)
        
    def get_themes(self) -> List[Theme]:
        return self.themes
    
    def get_assets(self) -> List[Asset]:
        return self.current.assets
    
    def load_theme(self, theme: Theme | str):
        if type(theme) is str:
            for i in self.themes:
                if i.name == theme:
                    theme = i
        self.current = theme
    
    # to get a theme color:
    # preview = themes.get_themes()
    # themes = []
    # for i in preview:
    #      themes.append(preview.name)
    # (pick theme here)
    # themes.load_theme(picked)
    # (you should know which colors it has)
    # themes.get_termcol()
    
    def create_themefile(self, path):
        self.storage["DEFAULT"]["current_theme"] = "default"
        self.new_theme(self.default_theme)
        self.save()
    
    def get_termcol(self, asset: Asset) -> str:
        # fg: \x1b[38;2;r;g;bm
        # bg: \x1b[48;2;r;g;bm
        bg = "38" if asset.fg else "48"
        return f"\x1b[{bg};2;{asset.r};{asset.g};{asset.b}"
    
    def load_themefile(self, path):
        self.themefile = path
        if not os.path.exists(path):
            self.create_themefile(path)
        self.load()
        
class ThemeUI:
    def __init__(self, handler: ThemeHandler):
        self.handler = handler
        self.current = handler.current
    
    def run_menu(self):
        while(True):
            rows, cols = get_terminal_size()
            action = read_key()
            
            box_h = 10 # TODO: set dynamically
            box_w = 32
            
            box_x = cols - box_w
            box_y = rows - box_h
            
            goto(box_x, box_y)
            print("action", action)