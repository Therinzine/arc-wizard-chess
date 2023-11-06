import chess

class Path:
    def __init__(self, piece: str, points: list) -> None:
        self.piece = piece
        self.points = points
   
    def __repr__(self):
        return f'{self.piece}: {self.points}'

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
            if self.board.is_kingside_castling(move):
                paths.append(Path(piece_id, self.single_path(move.from_square, move.to_square)))
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
     
        startRank = chess.square_rank(start)
        startFile = chess.square_file(start)
        endRank = chess.square_rank(target)
        endFile = chess.square_file(target)
        changeInRank = endRank - startRank
        changeInFile = endFile - startFile
        moveInbetween = False

    #Knight path planning 1 path, not both paths. Check to see if it moves in a knight pattern

        moveInbetween = False 
        if ((abs(changeInRank) == 2 and abs(changeInFile) == 1) or (abs(changeInFile) == 2 and abs(changeInRank) == 1)):
            rankDirection = 1 if changeInRank > 0 else -1
            fileDirection = 1 if changeInFile > 0 else -1
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
                changeInRank = startRank + 2 * rankDirection
                #changeFile = startFile + fileDirection
                changeSquare = chess.square(startFile, changeInRank)
            else:
                #changeRank = startRank + rankDirection
                changeFile = startFile + 2 * fileDirection
                changeSquare = chess.square(changeFile, startRank)
            #pretty janky way to do this, find a cleaner way to get back to middle square.
            if moveInbetween == True:
                return [(chess.square_file(location) + 1, chess.square_rank(location) + 1) for location in [start, changeSquare, target]]
                
            else:
                return [(chess.square_file(location) + .5, chess.square_rank(location) + .5) for location in [start, changeSquare, target]]


        #Castle this means that the rook is moving, need to move the rook around
        if move_type == "CASTLE":
            return[(chess.square_file(location) + 1, chess.square_rank(location) + 1) for location in [start, target]]
                
        #Capture Position, if this piece is capturing something. Will always move it back to same position (Top left, i think?). Does not move back to center of square. This done here or in other path?
        if (target > 63):
            return [(chess.square_file(location) + 1, chess.square_rank(location) + 1) for location in [start, target]]
        else:
            return [(chess.square_file(location) + .5, chess.square_rank(location) + .5) for location in [start, target]]
                


