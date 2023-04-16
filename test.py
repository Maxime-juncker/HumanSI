import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__) + "/../util"))
from Utilities import *
from pyglet.window import Window
from pyglet import app, shapes
import pyglet
window = Window(width=1920, height=1080)
window.set_location(0, 0)
batch = pyglet.graphics.Batch()

import pyglet

screen_size = screen_width, screen_height = 400, 400
center_x, center_y = screen_width/2, screen_height/2
radius = 200

green = (64, 160, 43)
blue = (30, 102, 245)
mauve = (136, 57, 239)

def load_animation(entity, state, frames):
    images = [pyglet.image.load("../assets/sprites/{e}/{s}/{e}-{s}-{x:02}.png".format(x=x, e=entity, s=state)) for x in range(frames)]

    for image in images:
        image.anchor_x = image.width // 2
        image.anchor_y = image.height // 2

    frames = [pyglet.image.AnimationFrame(x, duration=0.1) for x in images]
    return pyglet.image.Animation(frames=frames)


# Image
goblin_image = pyglet.image.load(Directories.SpritesDir + "Civilisations/Yellow/BuildingsYellow/HDV/HdvD1.png")
goblin_image.anchor_x = goblin_image.width // 2
goblin_image.anchor_y = goblin_image.height // 2

# Sprite
goblin = pyglet.sprite.Sprite(
    goblin_image,
    x=center_x,
    y=center_y,
    batch=batch
)

# Flip horizontally
goblin.scale_x = -1

# rotate slightly to go uphill
goblin.rotation = 8

@window.event
def on_draw():
    window.clear();
    batch.draw();

app.run()
