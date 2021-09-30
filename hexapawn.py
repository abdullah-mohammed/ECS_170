#Abdullah Mohammed 914923231
import copy 
import operator 

#PARAMETERS: board = initial board passed in, boardSize = size of nxn board, team = what side we're playing on, 
#movesAhead = number of moves ahead our minimax search looks 
#OUTPUTS: returns the next best move using the above information 
def hexapawn(board, boardSize, team, movesAhead):
    #make the root element here 
    if team == 'w':
        turn = 'b'
    elif team == 'b':
        turn = 'w'

    if 0 == movesAhead:
        boardVal = staticBoardEvaluation(board, team, boardSize, turn)
    else :
        boardVal = None
    
    rootNode = Node(board, None, boardVal, 0)
    #generate tree here and minimax occurs in this function 
    generateTree(rootNode, boardSize, team, movesAhead, team, 0)

    #edge case handling 
    if len(rootNode.children) == 0:
        return rootNode.board #returns the board that was passed with no changes 

    #find and return max value from roots children (since root is always max and board values have already been propogated up) 
    sortedRootChildren = sorted(rootNode.children, key= operator.attrgetter('boardValue'))
    maxItr = len(sortedRootChildren) - 1
    
    return sortedRootChildren[maxItr].board

            
#node object used to store the board, the parent node, the static board value, the level, and the possible next moves(children)
class Node: 
    def __init__(self, board, parent, boardVal, level):
        self.parent = parent
        self.board = board 
        self.level = level
        self.boardValue = boardVal
        self.children=  []


#MINIMAX FUNCTION
#PARAMETERS: parent Node, size of board, team to generate moves for, moves to look ahead, the team we're playing, the number of moves we have searched(level)
#OUTPUTS: modifies the parent originally passed in and fully constructs the tree with the information given above
#This function generates the tree with respect to the number of moves ahead to look, and after the tree is generated it propogates the proper board values as specificed in the minimax procedure
def generateTree(parent, boardSize, team, movesAhead, originalTeam, level):
    if level == movesAhead:
        return 
    
    #turn is always opposite of team, this information is used to see if it's the players turn and they cannot move in the static board evaluation 
    if team == 'w':
        newTurn = 'b'
    elif team == 'b':
        newTurn = 'w'

    #create children 
    newNodes = createNodes(parent, boardSize, team, newTurn, level + 1, originalTeam, movesAhead)

    parent.children = newNodes

    #traverse all children 
    for vals in newNodes:
        #alternate whose move it is 
        if team == 'w':
            newTeam = 'b'
        elif team == 'b':
            newTeam = 'w'

        generateTree(vals, boardSize, newTeam, movesAhead, originalTeam, level + 1)
    
    #MINIMAX PROCEDURE OCCURS HERE 
    if len(newNodes) != 0:
        #check if all boardValues have been filled before proceeding
        allValuesAssigned = 1 #true 
        for val in newNodes:
            if val.boardValue == None:
                allValuesAssigned = 0 #false

        if allValuesAssigned == 1:
            #sort the children from least to greatest 
            sortedChildren = sorted(newNodes, key= operator.attrgetter('boardValue'))
            if level % 2 == 0: #max level, get max of children
                #max will be last element 
                maxItr = len(sortedChildren) - 1
                parent.boardValue = sortedChildren[maxItr].boardValue
            elif level%2 == 1: #min level, get min of children 
                #min will be first element 
                parent.boardValue = sortedChildren[0].boardValue


#PARAMETERS: parent Node, size of board, the current players turn(team),
#turn is always opposite of current player and only used to see if the game is won on the condition that it is the opposite players turn and they cannot move
#level to be assigned to children (newLevel), the team we are playing, the number of moves ahead we are looking
#OUTPUTS: outputs all the children of parentNode in node format
#This function generates all the next moves when given a parentNode, converts them to a list of nodes, and changes all their board values if they are leaf nodes 
def createNodes(parentBoard, boardSize, team, turn, newLevel, originalTeam, movesAhead):
    newStates = generateAllNewMoves(parentBoard.board, team, boardSize)
    if len(newStates) == 0: #parentBoard is leaf node so need to assign static board value 
        if turn == 'w':
            prevTurn = 'b'
        elif turn == 'b':
            prevTurn = 'w'
        boardValue = staticBoardEvaluation(parentBoard.board, originalTeam, boardSize, prevTurn)
        parentBoard.boardValue = boardValue
        return []
    
    newNodes = [] 

    for newBoard in newStates:
        if newLevel == movesAhead: #we're at the leaf nodes 
            boardValue = staticBoardEvaluation(newBoard, originalTeam, boardSize, turn)
        else:
            boardValue = None
        
        nodeInsert = Node(newBoard, parentBoard, boardValue, newLevel)
        newNodes.append(nodeInsert)

    return newNodes


#BOARD EVALUATOR 
#PARAMETERS: board, what side we're playing on(team), the size of the board, turn value is always opposite of the team the board is generated for 
#OUTPUTS: returns the static board value from our calculations 
#the way the function calculates the value is:
#if we have won +10, if we lose -10, if nobody has won then boardValue = num of our pawns - num opponent pawns 
def staticBoardEvaluation(board, team, boardSize, turn): 
    winValue = gameWon(board, team, boardSize, turn)
    if winValue == 1:
        return 10
    elif winValue == -1:
        return -10

    wCounter = 0 
    bCounter = 0
    for rowItr in range(0, boardSize):
        for colItr in range(0, boardSize):
            if board[rowItr][colItr] == 'w':
                wCounter = wCounter + 1
            elif board[rowItr][colItr] == 'b':
                bCounter = bCounter + 1
    
    if team == 'w':
        difference = wCounter - bCounter
        return difference
    elif team == 'b':
        difference = bCounter - wCounter
        return difference


#PARAMETERS: board, team we are playing for, size of board, whoevers turn is next 
#OUTPUTS: returns 1 if the game has been won, -1 if the game is lost, 0 if nobody has won 
#This function first checks to see if any pawns have reached the end, then checks if either side has no pawns on the board, and finally checks if its a players turn and they cannot move 
def gameWon(board, team, boardSize, turn):
    #check if pawn on end 
    wAtEnd = 0 #changes to 1 if w value at end of board 
    bAtEnd = 0 #changes to 1 if b value makes it to first row 

    for colItr in range(0, boardSize):
        #check if any W's at the end 
        if board[boardSize - 1][colItr] == 'w':
            wAtEnd = 1 

    for colItr in range(0, boardSize):
        if board[0][colItr] == 'b':
            bAtEnd = 1

    if team == 'w':
        if wAtEnd == 1:
            return 1 #game won 
        elif bAtEnd == 1:
            return -1 #game lost 
    elif team == 'b' :
        if bAtEnd == 1:
            return 1 #game won 
        elif wAtEnd == 1:
            return -1 #game lost 

    #check if no pawns
    wCounter = 0 
    bCounter = 0
    for rowItr in range(0, boardSize):
        for colItr in range(0, boardSize):
            if board[rowItr][colItr] == 'w':
                wCounter = wCounter + 1
            elif board[rowItr][colItr] == 'b':
                bCounter = bCounter + 1
    
    if team == 'w':
        if wCounter == 0:
            return -1 # game lost 
        elif bCounter == 0:
            return 1 #game won
    elif team == 'b':
        if bCounter == 0:
            return -1 #game lost
        elif wCounter == 0:
            return 1 #game won
    
    #check if no move can be made
    if team == 'w':
        #opponents turn to move but they cannot do so 
        if turn == 'b':
            movementVal = canMove(board, 'b', boardSize)
            if movementVal == 0:
                return 1 # w wins
        elif turn == 'w':
            movementVal = canMove(board, 'w', boardSize)
            if movementVal == 0:
                return -1 # w lost 
    elif team == 'b':
        #opponents turn to move but they cannot do so 
        if turn == 'w':
            movementVal = canMove(board, 'w', boardSize)
            if movementVal == 0:
                return 1 #b wins 
        elif turn == 'b':#our turn 
            movementVal = canMove(board, 'b', boardSize)
            if movementVal == 0:
                return -1 #b loses 

    return 0 #nobody has won or lost 
    

#PARAMETERS: board, team to see if they can move, size of board 
#OUTPUTS: returns 1 if team can move, returns 0 if team cannot move 
#This function iterates through the board to see if the respective team can move 
def canMove(board, team, boardSize):
    if team == 'w':
        for rowItr in range(0, boardSize):
            for colItr in range(0, boardSize):
                if board[rowItr][colItr] == 'w' :
                    if rowItr < boardSize - 1:
                        if board[rowItr + 1][colItr] == '-' :
                            return 1 #can move
                        elif colItr + 1 < boardSize:
                            if board[rowItr + 1][colItr + 1] == 'b':
                               return 1 #can move

                        elif colItr - 1 >= 0:
                            if board[rowItr + 1][colItr - 1] == 'b':
                                return 1 #can move
    elif team == 'b':
        for rowItr in range(0, boardSize):
            for colItr in range(0, boardSize):
                if board[rowItr][colItr] == 'b' :
                    if rowItr > 0:
                        if board[rowItr - 1][colItr] == '-':
                            return 1 #can move
                        elif colItr + 1 < boardSize:
                            if board[rowItr - 1][colItr + 1] == 'w':
                                return 1 #can move
                        elif colItr - 1 >= 0:
                            if board[rowItr - 1][colItr - 1] == 'w':
                                return 1 #can move

    return 0 #false, cannot move 


#MOVE GENERATOR 
#PARAMETERS: board, the team to generate moves for, the size of the board 
#OUTPUTS: returns a list of all the new moves that can be made by the respective team in board format
#This function traverses the board to generate possible new moves from the current board state
def generateAllNewMoves(board, team, boardSize):
    newMoves = []

    for rowItr in range(0, boardSize):
        for colItr in range(0, boardSize): 
            if team == 'w':
                if board[rowItr][colItr] == 'w' :
                    newBoards = generateIndividualMoveWhite(copy.deepcopy(board), boardSize, rowItr, colItr)
                    newMoves = newMoves + newBoards

            elif team == 'b':
                if board[rowItr][colItr] == 'b' :
                    newBoards = generateIndividualMoveBlack(copy.deepcopy(board), boardSize, rowItr, colItr)
                    newMoves = newMoves + newBoards
    
    return newMoves


#PARAMETERS: board, size of board, row index of white piece, column index of white piece 
#OUTPUTS: returns all the possible moves the white pawn at the specified index can do as a list of boards
#This function is given the location of a pawn on the board and generates all the possible moves it can do 
def generateIndividualMoveWhite(board, boardSize, row, col):
    newMoves = [] 

    if row >= boardSize - 1: #at end of board, game is won if here 
        return newMoves
    
    #check forward move is possible 
    if board[row + 1][col] == '-' :
        #create forward move
        newBoardForward = copy.deepcopy(board)
        newBoardForward[row] = newBoardForward[row][0:col] + '-' + newBoardForward[row][col+1:]
        newBoardForward[row + 1] = newBoardForward[row + 1][0:col] + 'w' + newBoardForward[row + 1][col+1:]
        newMoves.append(newBoardForward)
    
    #check right diagonal move is possible 
    if col + 1 < boardSize:
        if board[row + 1][col + 1] == 'b':
            newDiagR = copy.deepcopy(board)
            newDiagR[row] = newDiagR[row][0:col] + '-' + newDiagR[row][col+1:]
            newDiagR[row + 1] = newDiagR[row + 1][0:col + 1] + 'w' + newDiagR[row + 1][col+2:]
            newMoves.append(newDiagR)

    #check left diagonal is possible 
    if col - 1 >= 0:
        if board[row + 1][col - 1] == 'b':
            newDiagL = copy.deepcopy(board)
            newDiagL[row] = newDiagL[row][0:col] + '-' + newDiagL[row][col+1:]
            newDiagL[row + 1] = newDiagL[row + 1][0:col - 1] + 'w' + newDiagL[row + 1][col:]
            newMoves.append(newDiagL)

    return newMoves


#PARAMETERS: board, size of board, row index of black piece, column index of black piece
#OUTPUTS: returns all the possible moves the black pawn at the specified index can do as a list of boards
#This function is given the location of a pawn on the board and generates all the possible moves it can do 
def generateIndividualMoveBlack(board, boardSize, row, col):
    newMoves = []

    if row <= 0 : #game is won if pawn is here 
        return newMoves

    #check if forward move possible 
    if board[row - 1][col] == '-':
        newBoardForward = copy.deepcopy(board)
        newBoardForward[row] = newBoardForward[row][0:col] + '-' + newBoardForward[row][col+1:]
        newBoardForward[row - 1] = newBoardForward[row - 1][0:col] + 'b' + newBoardForward[row - 1][col+1:]
        newMoves.append(newBoardForward)
    
    #check right diagonal is possible 
    if col + 1 < boardSize:
        if board[row - 1][col + 1] == 'w':
            newDiagR = copy.deepcopy(board)
            newDiagR[row] = newDiagR[row][0:col] + '-' + newDiagR[row][col+1:]
            newDiagR[row - 1] = newDiagR[row - 1][0:col + 1] + 'b' + newDiagR[row - 1][col+2:]
            newMoves.append(newDiagR)
    
    #check left diagonal is possible 
    if col - 1 >= 0:
        if board[row - 1][col - 1] == 'w':
            newDiagL = copy.deepcopy(board)
            newDiagL[row] = newDiagL[row][0:col] + '-' + newDiagL[row][col+1:]
            newDiagL[row - 1] = newDiagL[row - 1][0:col - 1] + 'b' + newDiagL[row - 1][col:]
            newMoves.append(newDiagL)

    return newMoves
    
