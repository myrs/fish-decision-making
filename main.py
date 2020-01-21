from p5 import setup, draw, size, background, run, triangle, fill
import numpy as np
from fish import Fish


# width = 800
# height = 200
width = 1400
height = 800
# width = 300
# height = 300

fishes = [Fish(np.random.random() * width, np.random.random() * height,
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

    for fish in fishes:
        fish.update(fishes)
        # to test with one fish
        # fish.update_one(fishes)
        fish.show()


# run(frame_rate=25)
# run(frame_rate=200)
run()
