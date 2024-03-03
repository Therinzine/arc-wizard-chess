import wizboard
import chess
# import server

# ask for input
# chess bot moves?
# get path for moves
# command robots

class Game:
    def __init__(self, server):
        self.board = wizboard.WizBoard(server)

    def make_move(self, move: chess.Move):
        paths = self.board.push(move)
        for path in paths:
            path.piece.execute_path(path.points)
            path.piece.send_buffer()

    def run(self):
        while True:
            print(self.board)
            try:
                move = input(f'{"White" if self.board.turn == chess.WHITE else "Black"} move:')
                move = chess.Move.from_uci(self.board.parse_san(move).uci())
            except ValueError: 
                if move == 'quit':
                    break
                print("invalid move")
                continue
            
            self.make_move(move)

# server = server()
game = Game(server)
game.run()