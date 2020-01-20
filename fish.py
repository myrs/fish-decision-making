from p5 import Vector, stroke, circle
import numpy as np


class Fish():

    def __init__(self, x, y, width, height):
        self.position = Vector(x, y)

        # random initial speed
        vec = (np.random.rand(2) - 0.5) * 10
        self.velocity = Vector(*vec)

        self.max_speed = 17
        # self.max_speed = 10

        self.width = width
        self.height = height

    def get_angle_with_neighbor(self):
        """calculates angle between fish and it's closest neighbor"""
        # first, calculate vector, pointing to the closes fish
        # it's a vector, connecting both fish positions
        direction_to_neighbor = self.closest_neighbor.position - self.position
        # calculate angle as angle between fish velocity vector and
        # the direction to the neighbor
        # the angle need to be negative to rotate
        angle = direction_to_neighbor.angle - self.velocity.angle

        # ensure angle is always less, than pi to make
        # future calculations right
        if angle > np.pi:
            angle -= np.pi
        elif angle < -np.pi:
            angle += np.pi

        return angle

    def get_turning_angle(self):
        """calculate turning angle in rads/second"""
        # get angle
        angle = self.get_angle_with_neighbor()
        # put it in sinus function
        # TODO should we be that precise? maybe just 2 digits?
        result = 0.5091 * np.sin(0.9987 * angle + 0.0071) - 0.0519
        # result = 0.51 * np.sin(angle + 0.01) - 0.05

        return result

    def get_acceleration_for_neighbor(self):
        """calculate acceleration defined by the closes neighbor"""
        # first, get distance to the closes neighbor
        # distance_to_neighbor = np.linalg.norm(
        # self.closest_neighbor.position - self.position)

        distance_to_neighbor = self.position.distance(self.closest_neighbor.position)

        # get angle with the neighbor
        angle = self.get_angle_with_neighbor()
        # neighbor is in front when angle is between -pi/2 and pi/2
        neighbor_in_front = angle > -np.pi / 2 and angle < np.pi / 2

        # default acceleration is 0
        # acceleration = 0

        # if angle is between -0.194 to 0.194 - it's a dead zone for acceleration
        if angle > 0.194 or angle < -0.194:
            # if True:
            # cases:
            # 1. Strong attraction
            # -- when fish closer than 23.5 centimeters
            # -- and further, than 7.9 centimeters

            # point should be inside the ellipse
            # +=0.83666 sqrt(27 - x^2)
            x0 = self.position.x
            y0 = self.position.y

            is_close_enough = False

            # x is a position of fish to test
            # it should lie inside y = +- solution
            x = self.closest_neighbor.position.x
            y = self.closest_neighbor.position.y

            try:
                y1 = 0.1 * (10 * y0 - 7 * np.sqrt(-1 *
                                                  (x0 ** 2) + 2 * x0 * x - x ** 2 + 729))
                y2 = 0.1 * (10 * y0 + 7 * np.sqrt(-1 *
                                                  (x0 ** 2) + 2 * x0 * x - x ** 2 + 729))

                top = y1 if y1 >= y2 else y2
                bottom = y1 if y1 < y2 else y2

                is_close_enough = bottom < y < top
            except Exception:
                pass

            # if distance_to_neighbor <= 23.5 and distance_to_neighbor > 7.9:
            if is_close_enough and distance_to_neighbor > 7.9:
                # 1.1. If neighbor in front - accelerate towards it
                if neighbor_in_front:
                    acceleration = 2

                # 1.1. If neighbor in behind - decelerate
                else:
                    acceleration = -1.2
                    # acceleration = -0.8

            # 2. Strong repulsion (when fish closer than 4.06 centimeters)
            elif distance_to_neighbor < 4.06:
                if neighbor_in_front:
                    acceleration = -0.8

                # accelerate a little bit if there's someone directly behind us
                else:
                    acceleration = 0.4

        # 3. When fish is between 4.06 and 7.9 - do nothing
        # TODO maybe some random stuff??

        return acceleration

    def update(self, fishes):
        # TODO behaviour is a sum or this two things!
        # TODO - add random movement?
        # when fish has no effect of other neighbors

        # self.set_closest_neighbor(fishes)

        # standard acceleration depends on velocity (Fig. 2.D)
        # as -0.24x + 1.54
        standard_acceleration = -0.24 * self.velocity.magnitude + 1.54


        # get turning angle
        # turning_angle = self.get_turning_angle()
        # get acceleration
        # neighbor_acceleration = self.get_acceleration_for_neighbor()
        walls_acceleration = self.get_walls_acceleration()

        # acceleration is a sum of accelerations influenced
        # by neighbor and by walls
        # acceleration = standard_acceleration + neighbor_acceleration + walls_acceleration
        acceleration = walls_acceleration + standard_acceleration 

        # change fish direction,
        # rotating velocity vector by the turning angle
        # (changes the object itself, returns None)
        # self.velocity.rotate(turning_angle)

        # change fish speed,
        # accelerating fish
        # find neighbor_acceleration vector
        self.velocity = self.velocity + self.velocity * acceleration / self.velocity.magnitude

        # TODO Rotation from wall after behaviour update?
        wall_rotation = self.get_wall_rotation()
        self.velocity.rotate(wall_rotation)  
        if wall_rotation:
            print('self.velocity')
            print(self.velocity)   

        # validate, that velocity has not passed the limit
        if self.velocity.magnitude > self.max_speed:
            self.velocity = self.max_speed * self.velocity / self.velocity.magnitude

        self.position += self.velocity


        # print(self.velocity)

        # self.ensure_in_bounds()

    def show(self):
        stroke(255)

        circle((self.position.x, self.position.y), radius=10)

    def set_closest_neighbor(self, fishes):
        closest = None
        closest_distance = np.inf
        for neighbor in fishes:
            # skip self!
            if self == neighbor:
                continue

            distance = self.position.distance(neighbor.position)
            if distance < closest_distance:
                closest_distance = distance
                closest = neighbor

        self.closest_neighbor = closest

        # self.closest_neighbor = min(
        # fishes, key=lambda f: np.linalg.norm(f.position - self.position))

    def reflect(self, vector):
        return vector - 2 * Vector(*vector.dot(self.edge_vector) * self.edge_vector)

    def get_walls_acceleration(self):
        walls_acceleration = 0
        # close to the wall

        edge_vector = self.get_edge_vector(delta=0, add_rotation=False)
        angle = self.velocity.angle - edge_vector.angle

        distance = self.velocity.distance(edge_vector)
        # if angle < 0.5 or angle > np.pi - 0.5 and distance < 15:
        # if angle < 0.5 and distance < 15:
        #     print('acceleration from wall')
        #     walls_acceleration = 1
        # else:
        #     print('decelerate')
        #     walls_acceleration = -0.5


        # # if fish is close to the wall
        # if self.position.x - delta < 0:
        #         or self.position.x + delta > self.width \
        #         or self.position.y - delta < 0 \
        #         or self.position.y + delta > self.height:
        #     print('decelerate')
        #     # 
        #     walls_acceleration = -0.5

        return walls_acceleration

    def get_edge_vector(self, delta=0, add_rotation=True):
        edge_vector = Vector(*np.zeros(2))

        # bounce from left wall
        if self.position.x - delta <= 0:
            self.position.x = 0
            edge_vector.x = 1
            # add a little rotation to avoid wall
            # if add_rotation:
            #     edge_vector.x += 0.1

        # bounce from right wall
        elif self.position.x + delta >= self.width:
            self.position.x = self.width
            edge_vector.x = -1
            # if add_rotation:
            #     edge_vector.x += -0.1

        # bounce from bottom wall
        if self.position.y - delta <= 0:
            self.position.y = 0
            edge_vector.y = 1
            # if add_rotation:
            #     edge_vector.y += 0.1

        # bounce from top wall
        elif self.position.y + delta >= self.height:
            self.position.y = self.height
            edge_vector.y = -1
            # if add_rotation:
            #     edge_vector.y += -0.1

        return edge_vector

    def get_wall_rotation(self):
        wall_rotation = 0
        edge_vector = self.get_edge_vector()


        # set rotation if close to edge
        if edge_vector.magnitude:
            print('Uebalas!!')
            print(self.position)
            print(edge_vector)
            # rotation is angle between edge vector and velocity
            # wall_rotation = edge_vector.angle - self.velocity.angle
            angle_with_vector = edge_vector.angle - self.velocity.angle
            
            if angle_with_vector > np.pi or angle_with_vector < -np.pi:
                wall_rotation = -np.pi / 2 - 0.15
            else:
                wall_rotation = np.pi / 2 + 0.15

            # wall_rotation = edge_vector.angle - self.velocity.angle
            print(wall_rotation)

        return wall_rotation

    def ensure_in_bounds(self):
        # bounce from left wall
        if self.position.x <= 0:
            self.position.x = 0

        # bounce from right wall
        elif self.position.x > self.width:
            self.position.x = self.width

        # bounce from bottom wall
        if self.position.y < 0:
            self.position.y = 0

        # bounce from top wall
        elif self.position.y > self.height:
            self.position.y = self.height

    # def bounce_from_edge_2(self):
    #     if self.position.x > self.width:
    #         self.position.x = 0
    #     elif self.position.x < 0:
    #         self.position.x = self.width

    #     if self.position.y > self.height:
    #         self.position.y = 0
    #     elif self.position.y < 0:
    #         self.position.y = self.height

        # return False

    # def bounce_from_edge(self):
    #     self.calculate_edge_vector()

    #     # edge vector is not 0 zero vector
    #     if self.edge_vector.magnitude:
    #         # fish should just "reflect from wall"
    #         self.velocity = self.reflect(self.velocity)

    #         return True

    #     return False
