import time
import argparse
import numpy as np

from p5 import setup, draw, size, background, run, triangle, fill, rect, line, quad
from fish import Fish


class Simulation:

    def __init__(self, fishes=4, replicas_top=0, replicas_bottom=0, follow_refugia_force=None):
        self.width = 1500
        # self.width = 1300
        self.height = 800

        # box parameters
        self.box_width = 120
        self.box_padding_left = 40
        self.box_left = self.width - self.box_width - self.box_padding_left
        self.box_top = 335

        self.fishes = fishes
        self.follow_refugia_force = follow_refugia_force
        self.replicas_top = replicas_top

        # replica outside
        # self.replica_initial_y_top = 320
        # self.replica_initial_y_bottom = 480
        # self.replica_final_y_top = 80
        # self.replica_final_y_bottom = 720

        # replica inside
        self.replica_initial_y_top = self.box_top + 20
        self.replica_initial_y_bottom = self.box_top + self.box_width - 20
        self.replica_final_y_top = 80
        self.replica_final_y_bottom = 720

        # decision line position
        self.decision_x = 520
        # shaded area position
        self.shaded_area_x = 280

        self.shoal = [Fish(self.get_starting_x(),
                           self.get_starting_y(),
                           self.width, self.height, self.shaded_area_x,
                           decision_x=self.decision_x,
                           follow_refugia_force=follow_refugia_force)
                      for _ in range(fishes)]

        self.replica_y_start = self.box_top + self.box_width / 2
        self.replica_x_start = self.width - self.box_padding_left - self.box_width / 2

        self.replicas_coordinates = []

        for i in range(replicas_top):
            self.add_replica(i, 'top')

        for i in range(replicas_bottom):
            self.add_replica(i, 'bottom')

    def add_replica(self, replica_id, position):
        x = self.get_replica_x(replica_id)
        y = self.get_replica_y(x, position)

        final_y = self.get_replica_y(0, position)
        # if position == 'top':
        #     final_y = self.replica_final_y_top
        # else:
        #     final_y = self.replica_final_y_bottom

        self.replicas_coordinates.append((x, y, final_y))

        replica = Fish(x, y, self.width, self.height, self.shaded_area_x,
                       replica=True, replica_final_y=final_y)
        self.shoal.append(replica)

    def get_replica_x(self, replica_id):
        # outside
        # return self.width - 10 - replica_id * 15
        # inside
        return self.width - self.box_padding_left - self.box_width / 2 - replica_id * 15

    def get_replica_y(self, x, position):
        # outside
        # x_initial = self.width
        # inside
        x_initial = self.width - self.box_padding_left - self.box_width / 2

        if position == 'top':
            return (self.replica_initial_y_top - self.replica_final_y_top) * x \
                / x_initial + self.replica_final_y_top
        else:
            return (self.replica_initial_y_bottom - self.replica_final_y_bottom) * x \
                / x_initial + self.replica_final_y_bottom

    def get_starting_x(self, position=None):
        return self.box_left + np.random.random() * self.box_width

    def get_starting_y(self, position=None):
        # random position
        return self.box_top + np.random.random() * self.box_width

    def draw_objects(self):
        # global simulation

        # triangle((0, 0), (0, 200), (350, 100))
        background(30, 30, 47)

        fill(50)
        # shaded are upper quadrant
        quad((0, 0), (0, 160), (280, 256), (self.shaded_area_x, 0))
        quad((0, self.height), (0, 640), (280, 544), (self.shaded_area_x, self.height))

        fill(102)
        triangle((0, 160), (0, 640), (700, 400))

        # fishes' start box
        rect((self.box_left, 335), self.box_width, self.box_width)

        # replica line
        for rc in self.replicas_coordinates:
            line((0, rc[2]), (rc[0], rc[1]))
        # line((0, 720), (self.replica_x_start, self.replica_y_start))

        # shaded area line
        line((self.shaded_area_x, 0), (self.shaded_area_x, self.height))

        # 544

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


def headless_simulation(fishes=2, replicas_top=0, replicas_bottom=0, follow_refugia_force=0.2):
    start = time.time()
    simulation = Simulation(fishes=fishes, replicas_top=replicas_top,
                            replicas_bottom=replicas_bottom, follow_refugia_force=follow_refugia_force)

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


def headless_simulations(shoals=20, fishes=2, replicas_top=0, replicas_bottom=0, follow_refugia_force=0.2):
    top_preference_proportions = []

    for i in range(shoals):
        print(f'\n\nShoal {i + 1} of {shoals}')
        top, bottom = headless_simulation(fishes=fishes, replicas_top=replicas_top,
                                          replicas_bottom=replicas_bottom,
                                          follow_refugia_force=follow_refugia_force)
        top_preference_proportion = top / fishes
        top_preference_proportions.append(top_preference_proportion)

    print(f'Proportions: {top_preference_proportions}')
    return top_preference_proportions

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--fishes", dest="fishes",
                        nargs='?', const=2, type=int, default=2,
                        help="define how many fishes will be used in simulation (default = 2)")
    parser.add_argument("-t", "--replicas_top", dest="replicas_top",
                        nargs='?', const=0, type=int, default=0,
                        help="define how many replicas_top will go top (default = 0)")

    parser.add_argument("-b", "--replicas_bottom", dest="replicas_bottom",
                        nargs='?', const=0, type=int, default=0,
                        help="define how many replicas_bottom will go bottom (default = 0)")

    args = parser.parse_args()
    print(args)
    print(args.fishes)

    simulation = Simulation(fishes=args.fishes,
                            replicas_top=args.replicas_top,
                            replicas_bottom=args.replicas_bottom)

    run()
    # run(frame_rate=25)
    # run(frame_rate=1000)
