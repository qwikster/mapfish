import configparser
import os
from dataclasses import dataclass
from typing import List, Optional

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
        
        self.storage = configparser.ConfigParser()
        self.default_theme = default_theme
    
    def save(self):
        with open(self.themefile, "w") as themefile:
            self.storage.write(themefile)
    
    def new_theme(self, theme):
        self.storage[theme.name] = {
            "name": theme.name,
            "author": theme.author,
        }
        for asset in theme.assets:
            self.storage[theme.name][asset.name] = f"{asset.r}, {asset.g}, {asset.b}, {str(asset.fg)}"
    
    def create_themefile(self, path):
        self.storage["DEFAULT"]["current_theme"] = "default"
        self.new_theme(self.default_theme)
        self.save()
        
    def load_themefile(self, path):
        self.themefile = path
        if not os.path.exists(path):
            self.create_themefile(path)
        print("work")
        input()