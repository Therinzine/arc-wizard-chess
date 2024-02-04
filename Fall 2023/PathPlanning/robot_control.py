# import server
import math

COUNTS_PER_SQUARE = 100

class Robot():
    def __init__(self, id, position, angle):
        self.id = id
        self.position = position

        # Angle is measured counterclockwise from horizontal
        self.angle = angle
        self.initial_angle = angle

    # BYTE ARRAY FORMAT
    # First byte -> command (0 = move, 1 = turn)
    # 
    # Moving
    # - Second byte -> distance 
    #    (float distance in terms of squares or integer # of encoder counts?)
    #
    # Turning
    # - Second byte -> angle (in degrees)
        
    def move(self, distance):
        command = bytearray([0, int(distance)])
        # server.send_command(self.id, command)
    
    def turn(self, angle):
        # positive angle is counterclockwise, negative is clockwise
        # Negative numbers are represented with two's complement, to be interpreted by arduino
        command_angle = angle if angle >= 0 else 256 + angle
        command = bytearray([1, int(command_angle)])
        # server.send_command(self.id, command)
        self.angle += angle
        self.angle = self.angle % 360

    def turn_to(self, angle):
        angle = angle % 360
        turn_angle = angle - self.angle
        if turn_angle > 180:
            turn_angle = -360 + turn_angle
        elif turn_angle < -180:
            turn_angle = 360 + turn_angle
        
        self.turn(turn_angle)

    def move_to(self, position):
        if self.position[0] == position[0]:
            angle = 90 if position[1] > self.position[1] else -90
        else:
            angle = math.degrees(math.atan((position[1] - self.position[1]) / (position[0] - self.position[0])))

        if position[0] < self.position[0]:
            angle += 180
        self.turn_to(angle)
        self.move(math.dist(self.position, position))
        self.position = position

    def face_forward(self):
        self.turn_to(self.initial_angle)

    def execute_path(self, path_points):
        print(f'Moving: {self.id} from {self.position} to {path_points[-1]}')
        for point in path_points:
            self.move_to(point)
            print(self.position)
            print(self.angle)
            print(f"Moved to {point}")
        self.face_forward()
        print(self.position)
        print(self.angle)
        print("Finished Path")