# Main entry point
from mapfisher.map import render_map

#lat = 35.980056
#lon = 139.752389
lat, lon = 44.923095, -77.362277
# REPLACE THESE
# these are the coordinates from that one part in the lucky star op
# also should be challenging to render because japan

def entry():
    data = render_map(lat, lon)
    print(data)
    input()

if __name__ == "__main__":
    entry()