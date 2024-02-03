#send_command(id, bytearray)
import server

class Robot():
    def __init__(self, id, position, angle):
        self.id = id
        self.position = position
        self.angle = angle
        self.initial_angle = angle

    def move(self, distance):
        command = bytearray()
        server.send_command(self.id, command)
    
    def turn(self, angle):
        command = bytearray()
        server.send_command(self.id, command)
        # update self.angle

    def turn_to(self):
        pass    
    
    def move_to(self, position):
        # turn to target
        # go there
        pass

    def face_forward(self):
        self.turn_to(self.initial_angle)

    def execute_path(self, path_points):
        for point in path_points:
            self.move_to(point)
        self.face_forward()
        self.position = path_points[-1]