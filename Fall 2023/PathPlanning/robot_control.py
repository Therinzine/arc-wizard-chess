#send_command(id, bytearray)
import server

class Robot():
    def __init__(self, id):
        self.id = id
        # self.position = 
        # self.facing   = 
        #   (angle)

    def update_position(self, position):
        self.position = position

    def move(self, distance):
        command = bytearray()
        server.send_command(self.id, command)
    
    def turn(self, angle):
        command = bytearray()
        server.send_command(self.id, command)