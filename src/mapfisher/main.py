# Main entry point
from mapfisher.map import render_map
import random

# lat, lon = random.uniform(-50, 50), random.uniform(-180, 180)
# lat, lon = 35.980056, 139.752389
lat, lon = 43.56959052514097, -79.56972908588058
# lat, lon = 44.000000, -77.000000

# REPLACE THESE
# these are the coordinates from that one part in the lucky star op
# also should be challenging to render because japan

def entry():
    for i in range(10, 21):
        render_map(lat, lon, zoom = i, debug=False)

if __name__ == "__main__":
    entry()