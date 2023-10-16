import chess

class Waypoint:
    def __init__(self, piece: chess.PieceType, point: tuple) -> None:
        self.piece = piece
        self.point = point
    
    def __str__(self):
        return f'{self.piece}: {self.point}'

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
        waypoints += [Waypoint(self.board.piece_list[move.from_square], point) for point in self.single_path(piece_type, move.from_square, move.to_square)]

        return waypoints
    
    def single_path(self, piece_type:chess.PieceType, start:chess.Square, target:chess.Square, capture=False) -> list[tuple]:
        '''
        Given starting/target locations and a piece type, generate list of points
        a single piece needs to travel to
        
        Path should generally reflect how a player would move the piece
           - ex. diagonal vs straight and then right for a bishop
        
        Use self.board data to avoid other pieces on the board if necessary
        '''
     
        startRank = chess.square_rank(start)
        startFile = chess.square_file(start)
        endRank = chess.square_rank(target)
        endFile = chess.square_file(target)
        moveInbetween = False

    #Knight path planning 1 path, not both paths
        if piece_type == chess.KNIGHT:
            moveInbetween = False 
            #determines how the ranks change
            changeInRank = endRank - startRank
            changeInFile = endFile - startFile
            rankDirection = 1 if changeInRank > 0 else -1
            fileDirection = 1 if changeInFile > 0 else -1
            

            #TEST to check both paths:
            if (changeInRank == 2):

                #path 1: 2 file than 1 rank:

                currentFile = startFile
                #move file by 2, check if their are any pieces along way
                while(currentFile != endFile):
                    currentFile = currentFile + fileDirection
                    currentSquare = chess.square(currentFile, currentRank)
                    if self.board.piece_at(currentSquare) is not None:
                        moveInbetween = True
                        break
                #move rank by 1, check if their are any pieces along way. Do i even need to check this? This should be the last move and if it is the last move then it will be a capture??
                currentRank = startRank + rankDirection
                if self.board.piece_at(currentSquare) is not None:
                    moveInbetween = True


                #path 2:
            elif (changeInFile == 2):
                #this would check to see if it moves 
                theh
            #we can remove this check if we want
            else:
                print('Not a valid knight move!')


            #End test




            currentRank = startRank + rankDirection
            currentFile = startFile + fileDirection
            #go through each square and see if there is a piece on the square
            while ((currentRank != endRank) or (currentFile != endFile)):
                currentSquare = chess.square(currentFile, currentRank)
                #if at any point there is a piece on the path, move inbetween squares, end loop
                if self.board.piece_at(currentSquare) is not None:
                    endMiddle = chess.square(endRank - 0.5, endFile - 0.5) #need to fix this, used later but is janky
                    moveInbetween = True
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
                return [(chess.square_file(location) + 1, chess.square_rank(location) + 1) for location in [start, changeSquare, target, endMiddle]]
            else:
                return [(chess.square_file(location) + .5, chess.square_rank(location) + .5) for location in [start, changeSquare, target]]


        #Castle: 
            #Going to be a specific piece type

        #Capture Position: 
            #

        #Leaving: if square greater than 63, then it is leaving do x


        # First make path assuming nothing is in the way
        # Check if path is obstructed
        return [(chess.square_file(location) + .5, chess.square_rank(location) + .5) for location in [start, target]]