import chess
from path_planner import PathPlanner, get_rank, get_file
from robot_control import Robot

class WizBoard(chess.Board):
    def __init__(self) -> None:
        super().__init__()
        self.path_planner = PathPlanner(self)
        initial_board = ['R1', 'N1', 'B1', 'Q', 'K', 'B2', 'N2', 'R2',
                           'P1', 'P1', 'P3', 'P4', 'P5', 'P6', 'P7', 'P8'] + \
                          [''] * 32 + \
                          ['p1', 'p2', 'p3', 'p4', 'p5', 'p6', 'p7', 'p8',
                           'r1', 'n1', 'b1', 'q', 'k', 'b2', 'n2', 'r2'] + \
                          [''] * 32
            # - this is to keep track of which specific knight/bishop/rook is where, chess module only tracks kind of piece.
            # - this is important because there is more than one black knight robot for example
        
        self.piece_list = []
        for i, piece_id in enumerate(initial_board):
            if piece_id != '':
                position = (get_rank(i) + .5, get_file(i) + .5)
                robot = Robot(piece_id, position, angle=(-90 if get_rank(i) > 3 else 90))
            else:
                robot = None
            self.piece_list.append(robot)

        self.capture_counts = [0, 0]

    def get_capture_position(self):
        return chess.H8 + 1 + ((self.turn == chess.BLACK) * 16) + self.capture_counts[not self.turn]         

    def push(self, move: chess.Move) -> None:
        if self.is_capture(move):
            captured_position = self.get_capture_position()
            self.piece_list[captured_position] = self.piece_list[move.to_square]

            self.capture_counts[not self.turn] += 1

        # Handle Castle  (extra swaps)
        
        # Standard Moves
        self.piece_list[move.to_square] = self.piece_list[move.from_square]
        self.piece_list[move.from_square] = None

        super().push(move)

    def pop(self) -> None:
        super().pop()
        # update wizboard's data about specific pieces (pieces_list)