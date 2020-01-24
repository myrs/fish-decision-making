import numpy as np

from math import degrees
from p5 import Vector, stroke, circle
from utils import random_trunc


class Fish():

    def __init__(self, x, y, width, height, shaded_area_x, replica_final_y=80,
                 replica=False, decision_x=None, follow_refugia_force=None):
        self.position = Vector(x, y)
        self.replica = replica
        self.decision_x = decision_x
        self.decision = None
        self.reached_shaded_area = False
        self.shaded_area_x = shaded_area_x
        self.follow_refugia_force = follow_refugia_force

        self.second_neighbor_turn_coefficient = 0.2
        self.second_neighbor_accelerate_coefficient = 0.2

        vec = (np.random.rand(2) - 0.5) * 10
        if not replica:
            # random initial speed
            self.velocity = Vector(*vec)
            print(self.velocity.magnitude)
        else:
            # get speed from initial vector
            # speed = float(Vector(*vec).magnitude)
            speed = 8
            print('speed')
            print(speed)
            # set speed to direction of replica path
            self.velocity = Vector(-x, replica_final_y - y).normalize()
            self.velocity = self.velocity + self.velocity * speed

        self.max_speed = 17
        # self.max_speed = 10

        self.width = width
        self.height = height

    def update_replica(self):
        # print('update replica')
        acceleration = self.get_standard_acceleration()
        self.velocity = self.velocity + self.velocity * acceleration / self.velocity.magnitude

        self.position += self.velocity

    def update(self, fishes):
        # TODO behaviour is a sum or this two things!
        # TODO - add random movement?
        # when fish has no effect of other neighbors
        if self.replica:
            self.update_replica()
            return

        if self.reached_shaded_area:
            return

        # validate if fish crossed decision line the first time
        if not self.decision and self.position.x < self.decision_x:
            print('fish made decision!')
            self.decision = 'top' if self.position.y < self.height / 2 else 'bottom'
            print(f'decision: {self.decision}')

        if self.position.x < self.shaded_area_x:
            self.reached_shaded_area = True
            print('fish reached shaded area!')
            # put fish inside the shaded area
            self.velocity = Vector(0, 0)
            self.position.x = 10
            self.position.y = 10 if self.position.y < self.height / 2 else self.height - 10

            return

        self.set_closest_neighbors(fishes)

        standard_acceleration = self.get_standard_acceleration()

        # get turning angle
        turning_angle_closest = self.get_turning_angle_for_neighbor(self.first_closest)
        turning_angle_2nd_closest = self.get_turning_angle_for_neighbor(
            self.second_closest, coefficient=self.second_neighbor_turn_coefficient)

        # turning_angle = turning_angle_closest
        turning_angle = turning_angle_closest + turning_angle_2nd_closest

        # angle for left wall direction
        # all fishes are experimenting the same attraction to the left wall

        if self.position.y < 400:
            left_border_vector = Vector(0, 80)
        else:
            left_border_vector = Vector(0, 720)

        if self.follow_refugia_force:
            direction_to_border = left_border_vector - self.position
            angle = self.get_angle_normalized(self.velocity.angle, direction_to_border.angle)
            left_wall_attraction = self.get_turning_angle(angle)

            turning_angle += left_wall_attraction * self.follow_refugia_force

        # if there are no neighbors
        elif turning_angle == 0:
            # turn a little bit randomly
            turning_angle = random_trunc(mean=0, sd=0.4, low=-10, upp=10)

        # change fish direction,
        # rotating velocity vector by the turning angle
        # (changes the object itself, returns None)
        self.velocity.rotate(turning_angle)

        # get acceleration
        # neighbor_acceleration = 0
        neighbor_acceleration_closest = self.get_acceleration_for_neighbor(
            self.first_closest)
        neighbor_acceleration_2nd_closest = self.get_acceleration_for_neighbor(
            self.second_closest, coefficient=self.second_neighbor_accelerate_coefficient)

        # this is not very exact, as acceleration should have directions?
        neighbor_acceleration = neighbor_acceleration_closest + neighbor_acceleration_2nd_closest

        walls_acceleration = self.get_walls_acceleration()

        # acceleration is a sum of accelerations influenced
        # by neighbor and by walls
        acceleration = standard_acceleration + neighbor_acceleration + walls_acceleration

        # change fish speed,
        # accelerating fish
        # find neighbor_acceleration vector
        self.velocity = self.velocity + self.velocity * acceleration / self.velocity.magnitude

        # validate, that velocity has not passed the limit
        if self.velocity.magnitude > self.max_speed:
            self.velocity = self.max_speed * self.velocity / self.velocity.magnitude

        self.position += self.velocity

        # after all updates are finished, ensure fish did not go out of edge
        # and adjust if necessary
        self.bounce_from_edge()

        self.bounce_from_obstacle()

    def update_one(self, fishes):
        # TODO behaviour is a sum or this two things!
        # TODO - add random movement?
        # when fish has no effect of other neighbors

        # standard acceleration depends on velocity (Fig. 2.D)
        # as -0.24x + 1.54
        standard_acceleration = -0.24 * self.velocity.magnitude + 1.54

        walls_acceleration = self.get_walls_acceleration()

        acceleration = standard_acceleration + walls_acceleration

        # change fish speed,
        # accelerating fish
        # find neighbor_acceleration vector
        self.velocity = self.velocity + self.velocity * acceleration / self.velocity.magnitude

        # validate, that velocity has not passed the limit
        if self.velocity.magnitude > self.max_speed:
            self.velocity = self.max_speed * self.velocity / self.velocity.magnitude

        self.position += self.velocity

        # after all updates are finished, ensure fish did not go out of edge
        # and adjust if necessary
        self.bounce_from_edge()

        self.bounce_from_obstacle()

    def get_standard_acceleration(self):
        # standard acceleration depends on velocity (Fig. 2.D)
        # as -0.24x + 1.54
        standard_acceleration = -0.24 * self.velocity.magnitude + 1.54
        standard_acceleration = random_trunc(
            mean=standard_acceleration, sd=0.3, low=-10, upp=20)

        return standard_acceleration

    def normalize_angle(self, angle):
        # ensure angle is always less, than pi to make
        # future calculations right
        if angle > np.pi:
            angle -= 2 * np.pi
        elif angle < -np.pi:
            angle += 2 * np.pi

        return angle

    def get_angle_normalized(self, ange_from, angle_to):
        """Return angle, that's always between -pi < angle < pi"""
        angle = angle_to - ange_from
        return self.normalize_angle(angle)

    def get_angle_with_neighbor(self, neighbor):
        """calculates angle between fish and it's closest neighbor"""
        # first, calculate vector, pointing to the closes fish
        # it's a vector, connecting both fish positions
        direction_to_neighbor = neighbor.position - self.position
        # calculate angle as angle between fish velocity vector and
        # the direction to the neighbor
        # the angle need to be negative to rotate
        return self.get_angle_normalized(self.velocity.angle, direction_to_neighbor.angle)

    def get_turning_angle(self, angle):
        # put it in sinus function
        # result = 0.5091 * np.sin(0.9987 * angle + 0.0071) - 0.0519
        # result = 0.49 * np.sin(0.97 * angle) - 0.06
        # $-0.49 \\cdot \\sin (0.97 \\cdot x + 0.00) + -0.06
        # turning_angle = 0.49 * np.sin(0.97 * angle) - 0.06
        # turning_angle = 0.49 * np.sin(0.97 * angle)
        # turning_angle = 0.51 * np.sin(angle + 0.01) - 0.05
        turning_angle = 0.51 * np.sin(angle + 0.01)

        turning_angle = random_trunc(mean=turning_angle, sd=0.1,
                                     low=turning_angle - 0.4, upp=turning_angle + 0.4)
        turning_angle = self.normalize_angle(turning_angle)

        return turning_angle

    def get_turning_angle_for_neighbor(self, neighbor, coefficient=1.0):
        """calculate turning angle in rads/second"""
        # get angle
        if neighbor is None:
            return 0

        turning_angle = 0
        
        angle = self.get_angle_with_neighbor(neighbor)
        distance = self.position.distance(neighbor.position)

        if distance < 100:
            turning_angle = self.get_turning_angle(angle)

            if distance > 50:
                # half strength if fish is far away
                turning_angle = turning_angle * 0.5

        # return turning_angle multiplied by neighbor coefficient
        return turning_angle * coefficient

    def get_acceleration_for_neighbor(self, neighbor, coefficient=1):
        """calculate acceleration defined by the closes neighbor"""
        # first, get distance to the closes neighbor
        # distance_to_neighbor = np.linalg.norm(
        # self.first_closest.position - self.position)
        if neighbor is None:
            return 0

        distance_to_neighbor = self.position.distance(neighbor.position)

        # get angle with the neighbor
        angle = self.get_angle_with_neighbor(neighbor)

        if angle > 0 and angle < np.pi / 2 \
                or angle < 0 and angle > -np.pi / 2:
            neighbor_in_front = True
        else:
            neighbor_in_front = False

        # neighbor_in_front = not neighbor_in_front

        # default acceleration is 0
        acceleration = 0

        # cases:
        # 1. Strong attraction
        if distance_to_neighbor > 10 and distance_to_neighbor <= 100:
            # 1.1. If neighbor in front - accelerate towards it
            if neighbor_in_front:
                if distance_to_neighbor > 25:
                    acceleration = random_trunc(mean=2, sd=0.25, low=1.5, upp=2.5)
                else:
                    acceleration = random_trunc(mean=1.5, sd=0.25, low=0.5, upp=1.5)

            # 1.1. If neighbor in behind - decelerate
            else:
                acceleration = random_trunc(mean=-1, sd=0.25, low=-1.5, upp=-0.5)

        # 2. Strong repulsion (when fish closer than 4.06 centimeters)
        elif distance_to_neighbor < 6:
            if neighbor_in_front:
                acceleration = random_trunc(mean=-1, sd=0.25, low=-1.5, upp=-0.5)

            # accelerate a little bit if there's someone directly behind us
            else:
                acceleration = random_trunc(mean=2, sd=0.25, low=1.5, upp=2.5)

        # 3. When fish is between 4.06 and 7.9 - do nothing
        # TODO maybe some random stuff??

        return acceleration * coefficient

    def show(self):
        stroke(255)

        circle((self.position.x, self.position.y), radius=10)

    def set_closest_neighbors(self, fishes):
        first_closest = None
        closest_distance = np.inf

        second_closest_distance = np.inf
        second_closest = None
        for neighbor in fishes:
            # skip self!
            if self == neighbor:
                continue

            # distance = self.position.distance(neighbor.position)
            # if distance < closest_distance:
            #     second_closest = first_closest
            #     second_closest_distance = closest_distance

            #     closest_distance = distance
            #     first_closest = neighbor

            # elif distance < second_closest_distance:
            #     second_closest = neighbor
            #     second_closest_distance = distance

            # we should be able to see this neighbor!
            # as fish vision is not 360 degrees
            angle = self.get_angle_with_neighbor(neighbor)
            # blind_front = 0
            blind_back = np.pi / 15

            if angle < np.pi - blind_back and angle > -np.pi + blind_back:
                distance = self.position.distance(neighbor.position)
                if distance < closest_distance:
                    second_closest = first_closest
                    second_closest_distance = closest_distance

                    closest_distance = distance
                    first_closest = neighbor

                elif distance < second_closest_distance:
                    second_closest = neighbor
                    second_closest_distance = distance
            else:
                pass
                # print('can\'t see a neighbor! ignore this guy')

        self.first_closest = first_closest
        self.second_closest = second_closest

    def reflect(self, vector):
        return vector - 2 * Vector(*vector.dot(self.edge_vector) * self.edge_vector)

    def get_walls_acceleration(self):
        walls_acceleration = 0
        distance = 15

        # get edge vector considering maximum reaction distance
        # of 15 centimeters
        edge_vector = self.get_edge_vector(distance=distance)
        angle = edge_vector.angle_between(self.velocity)


        # close to the wall
        if edge_vector.magnitude:
            # is in "escaping the wall" mode
            # when angle between fish and wall is small
            if np.pi / 2 - np.pi / 6 < angle < np.pi / 2 + np.pi / 6:
                walls_acceleration = random_trunc(mean=2, sd=0.5, low=1, upp=3)
                # walls_acceleration = 1
            
            # approaching to the wall
            elif angle > np.pi / 2 or angle < -np.pi / 2:
                walls_acceleration = random_trunc(mean=-0.5, sd=0.1, low=-1, upp=0)

        return walls_acceleration

    def get_edge_vector(self, distance=15):
        edge_vector = Vector(*np.zeros(2))

        # close to the left wall
        if self.position.x - distance <= 0:
            edge_vector.x = 1

        # close to the !top wall
        if self.position.y - distance <= 0:
            edge_vector.y = -1

        # close to the right wall
        elif self.position.x + distance >= self.width:
            edge_vector.x = -1

        # close to the !bottom wall
        elif self.position.y + distance >= self.height:
            edge_vector.y = 1

        # if obstacle is close
        p3 = np.asarray((self.position.x, self.position.y))
        p2 = np.asarray((700, 400))

        p1 = np.asarray((0, 160))
        distance_top_obstacle = np.linalg.norm(
            np.cross(p2 - p1, p1 - p3)) / np.linalg.norm(p2 - p1)

        # we can give priority to obstacle as at the left wall
        # fish is not active anyway?
        if distance_top_obstacle < distance:
            edge_vector = Vector(0.35, -0.94)

        p1 = np.asarray((0, 640))
        distance_bottom_obstacle = np.linalg.norm(
            np.cross(p2 - p1, p1 - p3)) / np.linalg.norm(p2 - p1)

        # we can give priority to obstacle as at the left wall
        # fish is not active anyway?
        if distance_bottom_obstacle < distance:
            edge_vector = Vector(0.35, 0.94)

        return edge_vector

    def bottom_obstacle_y(self, x):
        return -12 / 35 * x + 640

    def top_obstacle_y(self, x):
        return 12 / 35 * x + 160

    def bounce_from_obstacle(self):
        x0 = self.position.x
        y0 = self.position.y

        # define, if fish is inside the obstacle
        y_bottom = self.bottom_obstacle_y(x0)
        y_top = self.top_obstacle_y(x0)

        # inside triangle if y position is below y_bottom
        # and above y_top

        # top is what we see in the top
        # but it should be less, than 0, as coordinate start from top left angle
        if y_top < y0 < y_bottom:
            # print('in triangle!')
            top_vector = Vector(0.35, -0.94)
            bottom_vector = Vector(0.35, 0.94)

            # define if approached from top
            # angle between top vector and velocity (direction)
            # should be more than pi / 2 or less than pi / 2
            angle_with_top = self.get_angle_normalized(
                self.velocity.angle, top_vector.angle)

            angle_with_bottom = self.get_angle_normalized(
                self.velocity.angle, bottom_vector.angle)

            bounce_factor_angle = random_trunc(mean=0.1, sd=0.05, low=0.08, upp=0.2)

            # bounce from top
            if y0 - y_top < y_bottom - y0:
                # if abs(angle_with_top) > abs(angle_with_bottom):
                # if angle_with_top > np.pi / 2 or angle_with_top < -np.pi / 2:
                # print('approached from top!')
                # print(angle_with_top)
                bounce_vector = top_vector

                # define if bounce left or right
                # bounce left if angle is positive
                if angle_with_top > 0:
                    bounce_vector.rotate(-np.pi / 2)
                    bounce_vector.rotate(bounce_factor_angle)

                # bounce right if angle is negative
                else:
                    bounce_vector.rotate(np.pi / 2)
                    bounce_vector.rotate(-bounce_factor_angle)

                new_y = y_top

            # bounce from bottom
            else:
                # print('approached from bottom')
                bounce_vector = bottom_vector

                # define if bounce left or right
                # bounce left if angle is positive
                if angle_with_bottom > 0:
                    bounce_vector.rotate(-np.pi / 2)
                    bounce_vector.rotate(bounce_factor_angle)

                # bounce right if angle is negative
                else:
                    bounce_vector.rotate(np.pi / 2)
                    bounce_vector.rotate(-bounce_factor_angle)

                new_y = y_bottom

            rotation = self.get_angle_normalized(
                self.velocity.angle, bounce_vector.angle)
            # - self.velocity.angle
            self.velocity.rotate(rotation)

            # conserve x, but move to y0
            # maybe a more correct stuff can exist but this is good enough
            self.position.y = new_y

    def bounce_from_edge(self):
        bounce_vector = Vector(0, 0)
        # random between 0.1 and 0.2
        # bigger - fish spend less time close to the wall
        # separation = 0.15
        # variance = 0.15
        bounce_factor = random_trunc(mean=0.1, sd=0.05, low=0.05, upp=0.15)
        # print(bounce_factor)
        # bounce_factor = 0.1

        corner_delta = 10

        # bottom! wall
        if self.position.y > self.height:
            # print('from bottom wall!')
            self.position.y = self.height
            bounce_vector.y += -bounce_factor
            # vector heading down
            wall_vector = Vector(0, -1)
            angle = self.get_angle_normalized(self.velocity.angle, wall_vector.angle)

            if angle > 0:
                bounce_vector.x += -1
            else:
                bounce_vector.x += 1

            # reverse if close to x
            if self.position.x - corner_delta < 0 or self.position.x + corner_delta > self.width:
                # print('reverse!')
                bounce_vector.x = -bounce_vector.x

        # right wall
        if self.position.x > self.width:
            self.position.x = self.width
            bounce_vector.x += -bounce_factor
            # vector heading down
            wall_vector = Vector(-1, 0)
            angle = self.get_angle_normalized(self.velocity.angle, wall_vector.angle)

            if angle > 0:
                bounce_vector.y += 1
            else:
                bounce_vector.y += -1

        # top! wall
        if self.position.y < 0:
            self.position.y = 0
            bounce_vector.y += bounce_factor
            # vector heading down
            wall_vector = Vector(0, 1)
            angle = self.get_angle_normalized(self.velocity.angle, wall_vector.angle)

            if angle > 0:
                bounce_vector.x += 1
            else:
                bounce_vector.x += -1

            # reverse if close to x
            if self.position.x - corner_delta < 0 or self.position.x + corner_delta > self.width:
                # print('reverse!')
                bounce_vector.x = -bounce_vector.x

        # left wall
        if self.position.x < 0:
            self.position.x = 0
            bounce_vector.x += bounce_factor
            # vector heading down
            wall_vector = Vector(1, 0)
            angle = self.get_angle_normalized(self.velocity.angle, wall_vector.angle)

            if angle > 0:
                bounce_vector.y += -1
            else:
                bounce_vector.y += 1

        # bounce if there is edge vector
        if bounce_vector.magnitude:
            rotation = bounce_vector.angle - self.velocity.angle
            self.velocity.rotate(rotation)
