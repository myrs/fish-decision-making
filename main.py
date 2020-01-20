from p5 import setup, draw, size, background, run, triangle
import numpy as np
from fish import Fish


# width = 800
# height = 200
width = 800
height = 800

fishes = [Fish(np.random.random() * width, np.random.random() * height,
               width, height) for _ in range(18)]


def setup():
    # this happens just once
    size(width, height)  # instead of create_canvas


def draw():
    global fishes

    # triangle((0, 0), (0, 200), (350, 100))
    background(30, 30, 47)

    for fish in fishes:
        # fish.apply_behaviour(fishes)
        # fish.edges()
        fish.update(fishes)
        fish.show()


# run(frame_rate=25)
# run(frame_rate=200)
run()
