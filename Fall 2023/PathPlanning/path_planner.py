import chess

class Waypoint:
    def __init__(self, piece: chess.PieceType, point: tuple) -> None:
        self.piece = piece
        self.point = point

class PathPlanner():
    def __init__(self, board:chess.Board) -> None:
        self.board = board

    def turn_paths(self, move:chess.Move) -> list[Waypoint]:
        '''
        Given move, generate waypoints in the order that they should be traveled
            - Waypoints contain target location and active piece
            - ex. Capturing piece moves next to captured piece, captured piece
                  moves away, capturing piece moves to captured piece's spot 
        '''
        
        waypoints = []

        if not self.board.is_legal(move):
            return False
        
        # Handle Capture
        if self.board.is_capture(move):
            self.board.piece_at(move.to_square)
        # Handle Castle
        # Handle Standard moves
        piece_type = self.board.piece_at(move.from_square).piece_type
        waypoints += [Waypoint(self.board.piece_list[move.from_square], point) for point in self.path(piece_type, move.from_square, move.to_square)]

        return waypoints 
    
    def single_path(self, piece_type:chess.PieceType, start:chess.Square, target:chess.Square, capture=False) -> list[tuple]:
        '''
        Given starting/target locations and a piece type, generate list of points
        a single piece needs to travel to
        
        Path should generally reflect how a player would move the piece
           - ex. diagonal vs straight and then right for a bishop
        
        Use self.board data to avoid other pieces on the board if necessary
        '''

        # First make path assuming nothing is in the way
        # Check if path is obstructed
        return [(chess.square_file(location) + .5, chess.square_rank(location) + .5) for location in [start, target]]