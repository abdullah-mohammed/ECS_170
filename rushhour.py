#Abdullah Mohammed 914923231
import copy
import operator


#node object where I store the board state as well as other information 
class Node: 
    #expects a board state, a number representing depth of tree(level), list of Nodes of path to this node, and heuristic method choosing number 
    def __init__(self, board, level, prevVal, heuristic):
        self.prevVals = prevVal #all prior board states in tree that span back to the root(initial board call)

        if heuristic == 0: #run blocking heuristic
            self.hn = calculateFirstHn(copy.deepcopy(board))
        elif heuristic == 1: #run student heuristic
            self.hn = calculateSecondHn(copy.deepcopy(board))
        
        self.gn = level # g(n)
        self.fn = self.hn + self.gn # f(n)
        self.board = copy.deepcopy(board)
        self.futureStates = len(generateNewStates(copy.deepcopy(board))) #used to break ties if f(n) is same

#main function I call for this program 
#x is a number used to choose the heuristic, start is the initial board state formatted as a list of strings
#function doesn't return anything but prints the path of board states to the solution, the total moves, and the total states explored
def rushhour(x, start):
    unexplored = Node(start, 0, [], x)

    #tse represents total states explored
    solutionNode, tse = stateSearch([unexplored], [], 0, x)
    solutionPath = getBoardPathFromNodes(solutionNode)
    totalMoves = len(solutionPath) - 1 

    printSolutionPath(solutionPath)
    print("Total Moves: ", totalMoves)
    print("Total States Explored: ", tse)
    return

#printing entire path
#expects a list of board states and prints all of them 
def printSolutionPath(solutionPath):
    for board in solutionPath:
        printBoardPretty(board)

#printing individual board
#expects an individual board state and prints it
def printBoardPretty(board):
    for val in board:
        print(val)
    
    print("\n")

#gets the path of Nodes to the goal board state by traversing the prevVals attribute in the solution Node
#expects a solution Node and returns a list of boards that are in the path to the solution as well as the solution itself 
def getBoardPathFromNodes(solutionNode):
    solution = []
    for val in solutionNode.prevVals:
        solution.append(val.board)

    solution.append(solutionNode.board)

    return solution

#recursive function I call to find the solution Node that implements the A* algorithm 
#expects a list of unexplored boards in Node form, explored boards in board form, a number representing the level(total number of explored states), and the x val which chooses the heuristic
#returns a solution node with the path to the solution stored within it as well as other values stored in the Node object (gn, hn, fn, etc)
def stateSearch (unexplored, explored, level, x):
    if unexplored == []:
        return [], level
    else:
        if unexplored[0].hn == 0: #goal board state found 
            return unexplored[0], level 
        elif unexplored[0].board in explored : #checking for cycles
            result, tse = stateSearch(unexplored[1:], explored, level, x) #remove the repeated node and continue recursing
            return result, tse 

        else:
            newStates = generateNewStates(copy.deepcopy(unexplored[0].board)) #explore first node in unexplored and have new states in [board] form 

            newExplored = explored + [unexplored[0].board] 
            nodeGn = unexplored[0].gn #parent node tree depth
            newUnexplored = generateNodes(newStates, unexplored[0].prevVals + [unexplored[0]], nodeGn + 1, newExplored, x) #convert from [board] form to [Node] form 
            
            totalUnexplored = unexplored[1:] + newUnexplored

            #cycle checking 
            for allVals in totalUnexplored:
                if allVals.board in newExplored:
                    totalUnexplored.remove(allVals)

            #sort the unexplored nodes based on their f(n) value 
            sortedUnexplored = sorted(totalUnexplored, key= operator.attrgetter('fn'))

            #tie breaking nodes with the same lowest f(n) at the beginning of sortedUnexplored
            if len(sortedUnexplored) > 1 :
                if sortedUnexplored[0].fn == sortedUnexplored[1].fn: #at least one tie exists
                    sortedUnexplored = sortTiedVals(sortedUnexplored)

            result, tse = stateSearch(sortedUnexplored, newExplored, level + 1, x)
            return result, tse

#tie break by sorting nodes based on the number of future states they have 
#expects a list of Nodes that were sorted based on fn 
#returns a list of nodes originally sorted based on fn that are reordered to break ties if they share the lowest fn value in the original list
def sortTiedVals(sortedUnexplored):
    tiedFnVal = sortedUnexplored[0].fn
    index = 1 
    sortedTied = [sortedUnexplored[0]]

    #gets all values at the beginning of sortedUnexplored with the same lowest f(n)
    while sortedUnexplored[index].fn == tiedFnVal:
        sortedTied.append(sortedUnexplored[index])
        index = index + 1
        if index >= len(sortedUnexplored):
            index = -1
            break

    #sort based of future states 
    sortedTied = sorted (sortedTied, key = operator.attrgetter('futureStates')) 

    if index == -1 : #whole sortedUnexplored is the same f(n) and nothing to concatenate with 
        return sortedTied

    newSortedUnexplored = sortedTied + sortedUnexplored[index:]
    return newSortedUnexplored

#given an array of board states converts them to an array of Nodes 
#prevVal is the prior nodes in the path to the current nodes and level is depth of tree (g(n))
#expects a list of board states, all previous nodes in the path to these board states, the g(n), the states that have already been explored, and x value for choosing heuristic
#returns a list of nodes 
def generateNodes(newStates, prevVal, level, explored, x):
    newNodes = []
    
    for val in newStates:
        if val in explored: #cycle checking
            continue
        else:
            nodeInsert = Node(val, level, prevVal, x)
            newNodes.append(nodeInsert)
    
    return newNodes


#BLOCKING HEURISTIC 
#expects an individual board state 
#outputs a number that represents the h(n) value 
def calculateFirstHn(board):
    if board[2][5] == 'X':
        return 0
    else:
        hnVal = 1
        alreadyObserved = []
        #just added 
        firstX = 0 
        while board[2][firstX] != 'X':
            firstX = firstX + 1

        for colItr in range(firstX,6):
            if board[2][colItr] != 'X' and board[2][colItr] != '-':
                letter = board[2][colItr]
                if not letter in alreadyObserved:
                    hnVal=  hnVal + 1
                    alreadyObserved.append(board[2][colItr])

        return hnVal

#STUDENT HEURISTIC
#The way this heuristic works is it's a modified blocking heuristic that incorporates
#the distance from the special car to the end as well as how movable the cars blocking it are 

#The way this heuristic works is that it places greater importance (lower hn) on board states that 
#not only have less cars blocking their way as in the blocking heuristic, but boards where the special
#car is closer in distance to the end and boards where the cars blocking the special car are more movable

#when this heuristic is used on a board where there are not that many total states explored overall, the difference is less apparent
#than when there are a significant amount states explored when compared to the blocking heuristic.
#In cases where a larger amount of states are needed to be explored this heuristic shines in comparison to the blocking heuristic.
#Additionally, this heuristic is better than the blocking heuristic since the blocking one does not fully factor in the distance from the 
#special node to the end and the movability of vehicles blocking the special car. 

#expects an individual board state
#outputs a number corresponding to the h(n) value 
def calculateSecondHn(board): 
    if board[2][5] == 'X':
        return 0
    else:
        hnVal = 1
        alreadyObserved = []

        firstX = 0 
        while board[2][firstX] != 'X':
            firstX = firstX + 1

        distanceToEnd = 5 - firstX 
        hnVal = hnVal + distanceToEnd #incorporates the distance from the special car to the end (lower distance is better)

        for colItr in range(firstX,6):
            if board[2][colItr] != 'X' and board[2][colItr] != '-':
                letter = board[2][colItr]
                if not letter in alreadyObserved:
                    if board[1][colItr] == '-' or board[3][colItr == '-']: #incorporates how movable the vehicles blocking the way are 
                        #if the blocking vehicle can move(possibly) and is not stuck in place the board state is given a lower h(n)
                        hnVal = hnVal + 1
                    else:
                        hnVal = hnVal + 2

                    alreadyObserved.append(board[2][colItr])

        return hnVal

#generates all the new states possible from the current board and ouputs them in [board] form 
#expects an individual board state 
#outputs all the new states in a list of all new board states that can be made 
def generateNewStates(board):
    newStates = moveAllRight(copy.deepcopy(board)) + moveAllLeft(copy.deepcopy(board)) + moveAllUp(copy.deepcopy(board)) + moveAllDown(copy.deepcopy(board))

    return newStates

#generates all the board states where vehicles can move up 
#expects an individual board state 
#outputs a list of possible future board states 
def moveAllUp(board):
    alreadyVisited = []
    newUpStates = []

    for rowItr in range(0, 6):
        for colItr in range (0, 6):
            currLetter = board[rowItr][colItr]
            
            if (currLetter in alreadyVisited):
                continue
            else:
                alreadyVisited.append(currLetter)
                newBoard = moveUpIndividual(copy.deepcopy(board), rowItr, colItr) 
                
                if (newBoard != []):
                    newUpStates.append(newBoard)

    return newUpStates

#generates all the board states where vehicles can move down 
#expects an individual board state 
#outputs a list of possible future board states 
def moveAllDown(board):
    alreadyVisited = []
    newDownStates = []

    for rowItr in range(0, 6):
        for colItr in range (0, 6):
            currLetter = board[rowItr][colItr]

            if (currLetter in alreadyVisited):
                continue
            else:
                alreadyVisited.append(currLetter)
                newBoard = moveDownIndividual(copy.deepcopy(board), rowItr, colItr) 
                
                if (newBoard != []):
                    newDownStates.append(newBoard)

    return newDownStates

#generates all the board states where vehicles can move left 
#expects an individual board state 
#outputs a list of possible future board states 
def moveAllLeft(board):
    alreadyVisited = []
    newLeftStates = []

    for rowItr in range(0, 6):
        for colItr in range (0, 6):
            currLetter = board[rowItr][colItr]

            if (currLetter in alreadyVisited):
                continue
            else:
                alreadyVisited.append(currLetter)
                newBoard = moveLeftIndividual(copy.deepcopy(board), rowItr, colItr) 
                
                if (newBoard != []):
                    newLeftStates.append(newBoard)
    
    return newLeftStates

#generates all the board states where vehicles can move right 
#expects an individual board state 
#outputs a list of possible future board states 
def moveAllRight(board):
    alreadyVisited = []
    newRightStates = []

    for rowItr in range(0, 6):
        for colItr in range (0, 6):
            currLetter = board[rowItr][colItr]

            if (currLetter in alreadyVisited):
                continue
            else:
                alreadyVisited.append(currLetter)
                newBoard = moveRightIndividual(copy.deepcopy(board), rowItr, colItr) 
                
                if (newBoard != []):
                    newRightStates.append(newBoard)
    
    return newRightStates

#given a board state and a row and column with a letter on it moves that vehicle up if possible 
#expects an individual board state, a number representing row and a number representing column 
#outputs the new board state that can be made possibly by moving the vehicle at the the row and column value 
def moveUpIndividual(board, row, col):
    #cannot move up if already at the top 
    if row == 0:
        return []
    
    letter = board[row][col]

    #check if horizontal 
    if col == 0:
        if board[row][col + 1] == letter:
            return []
    elif col > 0 and col < 5 :
        if board[row][col + 1] == letter or board[row][col - 1] == letter:
            return []

    if board[row - 1][col] == '-':
        rowItr = row - 1
        while board[rowItr + 1][col] == letter:
            board[rowItr] = board[rowItr][:col] + letter + board[rowItr][col+1:]
            rowItr = rowItr + 1
            if rowItr == 5:
                break

        board[rowItr] = board[rowItr][:col] + '-' + board[rowItr][col+1:]
    else :
        return []
    

    return board

#given a board state and a row and column with a letter on it moves that vehicle down if possible
#expects an individual board state, a number representing row and a number representing column 
#outputs the new board state that can be made possibly by moving the vehicle at the the row and column value 
def moveDownIndividual(board, row, col):
    letter = board[row][col]

    #check if horizontal 
    if col == 0:
        if board[row][col + 1] == letter:
            return []
    elif col > 0 and col < 5 :
        if board[row][col + 1] == letter or board[row][col - 1] == letter:
            return []
    
    bottomIndex = row #initialize

    while (board[bottomIndex][col] == letter):
        bottomIndex = bottomIndex + 1
        if bottomIndex == 6:
            return [] #cant move down 
    

    if board[bottomIndex][col] == '-':
        while (board[bottomIndex - 1][col] == letter):
            board[bottomIndex] = board[bottomIndex][:col] + letter + board[bottomIndex][col+1:]
            bottomIndex = bottomIndex - 1
            
        board[bottomIndex] = board[bottomIndex][:col] + '-' + board[bottomIndex][col+1:]
    else :
        return[]
    
    return board

#given a board state and a row and column with a letter on it moves that vehicle left if possible
#expects an individual board state, a number representing row and a number representing column 
#outputs the new board state that can be made possibly by moving the vehicle at the the row and column value 
def moveLeftIndividual(board, row, col):
    #cant move left if at beginning 
    if col == 0:
        return []

    letter = board[row][col]

    #check if vertical 
    if col == 5:
        return []
    elif col > 0 and col < 5 :
        if board[row][col - 1] != letter and board[row][col + 1] != letter :
            return []
    elif col == 0: 
        if board[row][col + 1] != letter:
            return[]

    if board[row][col - 1] == '-':
        colItr = col - 1

        while board[row][colItr + 1] == letter :
            board[row] = board[row][:colItr] + letter + board[row][colItr+1:]
            colItr = colItr + 1
            if colItr == 5 :
                break
        
        board[row] = board[row][:colItr] + '-' + board[row][colItr+1:]
    else:
        return []
    
    return board

#given a board state and a row and column with a letter on it moves that vehicle right if possible
#expects an individual board state, a number representing row and a number representing column 
#outputs the new board state that can be made possibly by moving the vehicle at the the row and column value 
def moveRightIndividual(board, row, col):
    letter = board[row][col]

    #check if vertical 
    if col == 5:
        return []
    elif col > 0 and col < 5 :
        if board[row][col - 1] != letter and board[row][col + 1] != letter :
            return []
    elif col == 0: #testing rn 
        if board[row][col + 1] != letter:
            return[]


    rightmostVal = col

    while board[row][rightmostVal] == letter:
        rightmostVal = rightmostVal + 1
        if rightmostVal == 6:
            return [] #no space to move on right
    
    if board[row][rightmostVal] == '-':
        while board[row][rightmostVal - 1] == letter:
            board[row] = board[row][:rightmostVal] + letter + board[row][rightmostVal+1:]
            rightmostVal = rightmostVal - 1

        board[row] = board[row][:rightmostVal] + '-' + board[row][rightmostVal+1:]
    else :
        return []
    
    return board


#TEST CASES I used to test out my program 
#board = ["--AABB", "--CDEF", "XXCDEF", "--GGHH", "------", "------"] #given test in rubric
#board = ["---O--", "---O--", "XX-O--", "P-QQQ-", "P-----", "P-----"] 
#board = ["OOOP--", "--AP--", "XXAP--", "Q-----", "QGGCCD", "Q----D"] 
#board = ["--OPPP", "--O--A", "XXO--A", "-CC--Q", "-----Q", "--RRRQ"] 
#board = ["VV--ZZ", "--B---", "XXB---", "--B---", "------", "---YY-"] 

# rushhour(0, board)
# rushhour(1, board)
