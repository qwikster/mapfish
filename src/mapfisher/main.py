# Main entry point
from mapfisher.map import render_map
import random

# lat, lon = random.uniform(-90, 90), random.uniform(-180, 180)
# lat, lon = 35.980056, 139.752389
lat, lon = 44.505245, -77.472601
# lat, lon = 44.000000, -77.000000

# REPLACE THESE
# these are the coordinates from that one part in the lucky star op
# also should be challenging to render because japan

def entry():
    for i in range(10, 19):
        render_map(lat, lon, zoom = i)

if __name__ == "__main__":
    entry()