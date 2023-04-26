#!/usr/bin/env python
from Settings import WIDTH_RESOLUTION, HEIGHT_RESOLUTION
import math
from PIL import Image

im = Image.new('RGB', (WIDTH_RESOLUTION, 5))
ld = im.load()

# [distance, (r, g, b)]
heatmap = [
    [0.1, (0, 0, .4)],  # océan
    [0.2, (0, 0, .6)],  # océan peu profond
    [0.23, (.8, .4, 0)],  # plage
    [0.26, (.1, .5, .20)],  # plaine

    [0.4, (.1, .4, .1)],  # foret
    [0.6, (.1, .4, .1)],  # foret

    [0.7, (.3 ,.3, .3)],  # montagne
    [0.9, (.3, .3, .3)],  # montagne

    [1.00, (1.0, 1.0, 1.0)],  # sommet de la montagne
]


def gaussian(x, a, b, c, d=0):
    return a * math.exp(-(x - b) ** 2 / (2 * c ** 2)) + d


def pixel(x, width=100, map=[], spread=1):
    width = float(width)
    r = sum([gaussian(x, p[1][0], p[0] * width, width / (spread * len(map))) for p in map])
    g = sum([gaussian(x, p[1][1], p[0] * width, width / (spread * len(map))) for p in map])
    b = sum([gaussian(x, p[1][2], p[0] * width, width / (spread * len(map))) for p in map])
    return min(1.0, r), min(1.0, g), min(1.0, b)


def NewGradient():
    for x in range(im.size[0]):
        r, g, b = pixel(x, width=im.size[0], map=heatmap)
        r, g, b = [int(256 * v) for v in (r, g, b)]
        for y in range(im.size[1]):
            ld[x, y] = r, g, b

    im.save('grad.png')
    return im



NewGradient()
