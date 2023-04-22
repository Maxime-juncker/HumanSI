width, height = 1000, 200

import math
from PIL import Image

im = Image.open('./Assets/Graphics/Misc/GeneratedMap/terrain25.png')

org_size = im.size
pixelate_lvl = 8

# scale it down
im = im.resize(
    size=(org_size[0] // pixelate_lvl, org_size[1] // pixelate_lvl),
    resample=0)
# and scale it up to get pixelate effect
im = im.resize(org_size, resample=0)
im.show()