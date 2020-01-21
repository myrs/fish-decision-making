from p5 import setup, draw, size, background, run, triangle, fill, rect, line
import numpy as np
from fish import Fish


# width = 800
# height = 200
width = 1400
height = 800
# width = 300
# height = 300

box_width = 120
box_padding_left = 40
box_left = width - box_width - 40
# box_right = box_left + box_width

box_top = 335
# box_bottom = 335 + box_width

fishes = [Fish(box_left + np.random.random() * box_width, 
               box_top + np.random.random() * box_width,
               width, height) for _ in range(10)]

def setup():
    # this happens just once
    size(width, height)  # instead of create_canvas


def draw():
    global fishes

    # triangle((0, 0), (0, 200), (350, 100))
    background(30, 30, 47)

    fill(102)
    triangle((0, 160), (0, 640), (700, 400))

    rect((box_left, 335), box_width, box_width)

    line((0, 80), (width, 325))
    line((0, 720), (width, 475))

    for fish in fishes:
        fish.update(fishes)
        # to test with one fish
        # fish.update_one(fishes)
        fish.show()


# run(frame_rate=25)
# run(frame_rate=200)
run()
