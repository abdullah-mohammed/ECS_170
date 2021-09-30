#Abdullah Mohammed 914923231
import copy

def tilepuzzle(start,goal):
    return reverse(statesearch([start],goal,[]))


def statesearch(unexplored,goal,path):
    if unexplored == []:
        return []
    elif goal == head(unexplored):
        return cons(goal,path)
    else:
        #h(n) computations
        unexplored = sortWithHN(unexplored, goal)
        if head(unexplored) in path :
            unexplored.pop(0)

        result = statesearch(generateNewStates(head(unexplored)),
                             goal,
                             cons(head(unexplored), path))
        if result != []:
            return result
        else:
            return statesearch(tail(unexplored),
                               goal,
                               path)

def computeHN(stateExamined, goal):
    counter = 0
    for rowItr, rowVal in enumerate(stateExamined):
        for colItr, _ in enumerate(rowVal):
            if stateExamined[rowItr][colItr] != goal[rowItr][colItr]:
                counter = counter + 1
            
    return counter

def sortWithHN(unexplored, goal) :
    dictionary = {}

    for states in unexplored:
        hnVal = computeHN(states, goal) 
        tempTuple = tuple(map(tuple, states))
        dictionary[tempTuple] = hnVal

    sortedDictVals = sorted(dictionary.items(), key = lambda kv: kv[1])
    
    sortedUnexplored = []
    for tuples in sortedDictVals:
        convertedList = []
        
        for tupleConv in list(tuples[0]):
            convertedList.append(list(tupleConv))

        sortedUnexplored.append(convertedList)

    return sortedUnexplored

def generateNewStates(currState):
    rowVal, colVal = findLocation(currState)

    topMoves = generateTopMove(copy.deepcopy(currState), rowVal, colVal)
    bottomMoves = generateBottomMove(copy.deepcopy(currState), rowVal, colVal)
    rightMoves = generateRightMove(copy.deepcopy(currState), rowVal, colVal)
    leftMoves = generateLeftMove(copy.deepcopy(currState), rowVal, colVal)

    allNewStates = []
    if len(topMoves) > 0:
        allNewStates.append(topMoves)
    
    if len(bottomMoves) > 0:
        allNewStates.append(bottomMoves)
    
    if len(rightMoves) > 0:
        allNewStates.append(rightMoves)
    
    if len(leftMoves) > 0:
        allNewStates.append(leftMoves)
    

    return allNewStates


def findLocation(currState): 
    for rowVal, i in enumerate(currState):
        try:
            colVal = i.index(0)
        except ValueError:
            continue
        return rowVal, colVal

def generateTopMove(currState, rowVal, colVal):
    if rowVal == 0 :
        return []

    newRowVal = rowVal - 1
    switchVal = currState[newRowVal][colVal]
    currState[rowVal][colVal] = switchVal
    currState[newRowVal][colVal] = 0 

    return currState

def generateBottomMove(currState, rowVal, colVal) :
    if rowVal == 2:
        return []
    
    newRowVal = rowVal +  1
    switchVal = currState[newRowVal][colVal]
    currState[rowVal][colVal] = switchVal
    currState[newRowVal][colVal] = 0

    return currState

def generateLeftMove(currState, rowVal, colVal):
    if colVal == 0:
        return []
    
    newColVal = colVal - 1
    switchVal = currState[rowVal][newColVal]
    currState[rowVal][colVal] = switchVal
    currState[rowVal][newColVal] = 0

    return currState

def generateRightMove(currState, rowVal, colVal):
    if colVal == 2 :
        return []

    newColVal = colVal + 1
    switchVal = currState[rowVal][newColVal]
    currState[rowVal][colVal] = switchVal
    currState[rowVal][newColVal] = 0

    return currState


def reverse(st):
    return st[::-1]
    
def head(lst):
    return lst[0]

def tail(lst):
    return lst[1:]

def take(n,lst):
    return lst[0:n]

def drop(n,lst):
    return lst[n:]

def cons(item,lst):
    return [item] + lst
