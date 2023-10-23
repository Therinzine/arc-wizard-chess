import chess
from path_planner import PathPlanner

class WizBoard(chess.Board):
    def __init__(self) -> None:
        super().__init__()
        self.path_planner = PathPlanner(self)
        self.piece_list = ['r1', 'n1', 'b1', 'q', 'k', 'b2', 'n2', 'r2',
                           'p1', 'p1', 'p3', 'p4', 'p5', 'p6', 'p7', 'p8'] + \
                          [''] * 32 + \
                          ['P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7', 'P8',
                           'R1', 'N1', 'B1', 'Q', 'K', 'B2', 'N2', 'R2'] + \
                          [''] * 32
        
        self.capture_counts = [0, 0]
                           
        #                  "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
        # - this is to keep track of which specific knight/bishop/rook is where, chess module only tracks kind of piece.
        # - this is important because there is more than one black knight robot for example

    def push(self, move: chess.Move) -> None:
        if self.is_capture(move):
            captured_position = chess.H8 + ((move.color == chess.BLACK) * 16) + len(self.capture_counts[not move.color])
            self.piece_list[captured_position] = self.piece_list(move.to_square)

            self.capture_counts[not move.color] += 1

        # Handle Castle  (extra swaps)
        
        # Standard Moves
        self.piece_list[move.to_square] = self.piece_list[move.from_square]
        self.piece_list[move.from_square] = ''

        super().push(move)

    def pop(self) -> None:
        super().pop()
        # update wizboard's data about specific pieces (pieces_list)