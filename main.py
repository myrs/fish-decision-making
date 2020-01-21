import time
import numpy as np

from p5 import setup, draw, size, background, run, triangle, fill, rect, line
from fish import Fish

class Simulation:
    def __init__(self, fishes=4, replicas=2):        
        self.width = 1400
        self.height = 800
            
        # box parameters
        self.box_width = 120
        self.box_padding_left = 40
        self.box_left = self.width - self.box_width - 40
        self.box_top = 335

        self.fishes = fishes
        self.replicas = replicas

        # decision line position
        self.decision_x = 520

        self.shoal = [Fish(self.box_left + np.random.random() * self.box_width, 
                       self.box_top + np.random.random() * self.box_width,
                       self.width, self.height, decision_x=self.decision_x) for _ in range(fishes)]

        self.replica_y_start = self.box_top + self.box_width / 2
        self.replica_x_start = self.width - self.box_padding_left - self.box_width / 2

        for i in range(replicas):
            replica = Fish(self.replica_x_start, self.replica_y_start, self.width, self.height, replica=True)
            self.shoal.append(replica)

    def draw_objects(self):
        # global simulation

        # triangle((0, 0), (0, 200), (350, 100))
        background(30, 30, 47)

        fill(102)
        triangle((0, 160), (0, 640), (700, 400))

        # fishes' start box
        rect((self.box_left, 335), self.box_width, self.box_width)

        # replica line
        line((0, 80), (self.replica_x_start, self.replica_y_start))
        # line((0, 720), (self.replica_x_start, self.replica_y_start))

        # decision line
        line((self.decision_x, 0), (self.decision_x, self.height))

    def run_step(self, visualize=True):
        # global simulation

        if visualize:
            self.draw_objects()

        for fish in self.shoal:
            fish.update(self.shoal)
            # to test with one fish
            # fish.update_one(fishes)
            if visualize:
                fish.show()

        fishes_not_replica = list(filter(lambda f: not f.replica, self.shoal))
        top = len(list(filter(lambda f: f.decision == 'top', fishes_not_replica)))
        bottom = len(list(filter(lambda f: f.decision == 'bottom', fishes_not_replica)))

        total = top + bottom
        all_dicided = total == len(fishes_not_replica)

        return all_dicided, top, bottom

def setup():
    # global simulation
    # this happens just once
    size(simulation.width, simulation.height)  # instead of create_canvas

def draw():
    simulation.run_step()

def headless_simulation(fishes=4, replicas=0):
    start = time.time()
    simulation = Simulation(fishes=fishes, replicas=replicas)
    
    all_dicided = False
    step = 0
    
    while not all_dicided:
        step += 1
        print(f'step: {step}', end='\r')
        all_dicided, top, bottom = simulation.run_step(False)

    print(f'Decided top: {top}, decided bottom: {bottom}, steps: {step}')
    end = time.time()

    print(f'total time: {end - start:.2f}')
    return top, bottom

if __name__ == '__main__':
    # TODO add sys args!
    simulation = Simulation()
    
    run()
    # run(frame_rate=25)
    # run(frame_rate=1000)


