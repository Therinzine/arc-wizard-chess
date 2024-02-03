import chess

class Path:
    def __init__(self, piece: str, points: list) -> None:
        self.piece = piece
        self.points = points
   
    def __repr__(self):
        return f'{self.piece}: {self.points}'

def get_rank(square):
    return chess.square_rank(square) if square <=63 else chess.square_file(square)

def get_file(square):
    return chess.square_file(square) if square <=63 else chess.square_rank(square)

class PathPlanner():
    def __init__(self, board:chess.Board) -> None:
        self.board = board

    def turn_paths(self, move:chess.Move) -> list[Path]:
        '''
        Given move, generate Paths for in the order that they should be traveled
            - Paths contain active piece code (ex. 'p1') and list of points
            - ex. Capturing piece moves next to captured piece, captured piece
                  moves away, capturing piece moves to captured piece's spot 
        
        Returns list of tuples that contain (piece, [list of points])
        '''
        
        paths = []

        if not self.board.is_legal(move):
            return False
        
        piece_id = self.board.piece_list[move.from_square]

        # Handle Capture
        if self.board.is_capture(move):
            
            captured_position = chess.H8 + ((self.board.turn == chess.BLACK) * 16) + self.board.capture_counts[not self.board.turn]
            
            if self.board.is_en_passant(move):
                captured_piece_square = move.to_square + (8 * self.board.turn)
                captured_piece_id = self.board.piece_list[captured_piece_square]

                paths.append(Path(piece_id, self.single_path(move.from_square, move.to_square)))
                paths.append(Path(captured_piece_id, self.single_path(captured_piece_square, captured_position, move_type="LEAVE")))
                return paths
            else:
                captured_piece_id = self.board.piece_list[move.to_square]

                paths.append(Path(piece_id, self.single_path(move.from_square, move.to_square, move_type="CAPTURE")))
                paths.append(Path(captured_piece_id, self.single_path(move.to_square, captured_position, move_type="LEAVE")))
                paths.append(Path(piece_id, self.single_path(move.to_square, move.to_square)))
                return paths

        # Handle Castle
        if self.board.is_castling(move):
            paths.append(Path(piece_id, self.single_path(move.from_square, move.to_square)))
            if self.board.is_kingside_castling(move):
                paths.append(Path(piece_id, self.single_path(move.from_square + 3, move.from_square + 1, move_type="CASTLE")))
            else:
                paths.append(Path(piece_id, self.single_path(move.from_square - 4, move.from_square - 1, move_type="CASTLE")))
            return paths
                
        
        # Handle Standard moves
        paths.append(Path(piece_id, self.single_path(move.from_square, move.to_square)))

        return paths
    
    def single_path(self, start:chess.Square, target:chess.Square, move_type="NORMAL") -> list[tuple]:
        '''
        Given starting/target locations and a piece type, generate list of points
        a single piece needs to travel to
        
        Path should generally reflect how a player would move the piece
           - ex. diagonal vs straight and then right for a bishop
        
        Use self.board data to avoid other pieces on the board if necessary

        move_type: "NORMAL", "CASTLE", "CAPTURE", or "LEAVE"
        '''
        #Variables used for Knight movement
        startRank = get_rank(start) 
        startFile = get_file(start)
        endRank = get_rank(target)
        endFile = get_file(target)
        changeInRank = endRank - startRank
        changeInFile = endFile - startFile
        rankDirection = 1 if changeInRank > 0 else -1
        fileDirection = 1 if changeInFile > 0 else -1
        moveInbetween = False

        #Normal movement (includes knight move)
        if (move_type == "NORMAL"):

        #Knight movement: path planning 1 path, not both paths.
            if ((abs(changeInRank) == 2 and abs(changeInFile) == 1) or (abs(changeInFile) == 2 and abs(changeInRank) == 1)):
                currentRank = startRank + rankDirection
                currentFile = startFile + fileDirection
                #go through each square and see if there is a piece on the square
                while ((currentRank != endRank) or (currentFile != endFile)):
                    currentSquare = chess.square(currentFile, currentRank)
                    #if at any point there is a piece on the path, move inbetween squares, end loop
                    if self.board.piece_at(currentSquare) is not None:
                    # endMiddle = chess.square(endRank, endFile) #need to fix this, used later but is janky
                        moveInbetween = True
                        endMiddle = chess.square(endRank, endFile)
                        break
                    #should be one at a time, not both at once, fix this to check both paths
                    if (currentRank != endRank):
                        currentRank += rankDirection
                    if (currentFile != endFile):
                        currentFile += fileDirection
                #Locates the 'change square' of the L movement from the knight
                if (abs(changeInRank) == 2):
                    changeRank = startRank + (1.5 + 1 * (rankDirection == 1)) * rankDirection
                    changeFile = startFile + 1 * (fileDirection == 1) if moveInbetween else startFile + .5
                    #changeFile = startFile + fileDirection
                    startPosition = (changeFile, startRank + .5)
                    changePosition = (changeFile, changeRank)
                else:
                    #changeRank = startRank + rankDirection
                    changeFile = startFile + (1.5 + 1 * (fileDirection == 1)) * fileDirection
                    changeRank = startRank + 1 * (rankDirection == 1) if moveInbetween else startRank + .5
                    startPosition = (startFile + .5, changeRank)
                    changePosition = (changeFile, changeRank)
                #move in between squares and end up back in middle of square
                return [startPosition, changePosition, (endFile + .5, endRank + .5)]
        #Normal Movement: Movement for any piece not fitting the criteria of a special move
            else:
                return [(get_file(location) + 0.5, get_rank(location) + 0.5) for location in [start, target]]
    
    #Castle: Means that the rook is moving, need to move the rook inbetween squares
        elif move_type == "CASTLE":
            castleRank = startRank + 1 * (startRank == 0)
            t = [(startFile + .5, castleRank), (endFile + .5, castleRank), (endFile + .5, endRank + .5)]
            return t
                
    #Piece is Capturing: Moves to location of captured piece (could technically remove this)
        elif (move_type == "CAPTURE"):
            return [(get_file(location) + 0.5, get_rank(location) + 0.5) for location in [start, target]]
        
    #Piece is leaving the board: Moves inbetween squares and then back to center of square
        elif(move_type == "LEAVE"):
            leaveRank = startRank + 1 * (rankDirection == 1)
            t = [(startFile + .5, leaveRank), (endFile, leaveRank), (endFile, endRank + .5), (endFile + .5, endRank + .5)]
            return t
        
