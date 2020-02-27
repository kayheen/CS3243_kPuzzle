import os
import sys
import heapq 
import time
import math 
from copy import copy, deepcopy


class Puzzle(object):
    def __init__(self, init_state, goal_state):
        # you may add more attributes if you think is useful
        self.init_state = init_state
        self.goal_state = goal_state
        self.init_tuple = tuple(item for row in self.init_state for item in row)
        self.goal_tuple = tuple(item for row in self.goal_state for item in row)
        self.n = len(init_state)

        self.euclidDist = [[0 for i in self.goal_tuple] for j in self.goal_tuple]

        # use a tuple to identify the postion instead of a 2d array.
        # this stores a 2d array correspondence of currPostion to currValue and the corresponding euclidean distance   
        for currPos in range(len(self.goal_tuple)): # currPos represents position in currTuple 
            for numInGoal in range(len(self.goal_tuple)): # numInGoal represents a number (not a position)
                goalPos = self.goal_tuple.index(numInGoal) #this gets the index of the particulation number in the goal.
                self.euclidDist[currPos][numInGoal] = math.sqrt((goalPos//self.n - currPos//self.n) **2 +
                    (goalPos%self.n - currPos%self.n)**2)

        self.actions = list()
        

        self.numNodesGen = 0
        self.maxNumNodesInQ = 0
        self.time = 0

    def getBlank(self, state_tuple):
        return state_tuple.index(0)
        
    def getTuple(self, state, target):
        for i in range(self.n):
            for j in range(self.n):
                if state[i][j]==target:
                    return (i,j)
    def getGoalPos(self, targetNum):
        for i in range(len(self.goal_tuple)):
            if targetNum == self.goal_tuple[i]:
                return i

        return -1

    def euclideanHeu(self, state):
        finalHeu = 0
        # maxrange = self.n * self.n
        # for i in range(0, maxrange):
        #     (xInit, yInit) = self.getTuple(state, i)
        #     (xFinal, yFinal) = self.getTuple(self.goal_state, i)

        #     value = math.sqrt((xFinal - xInit)**2 + (yFinal - yInit)**2)
        #     #print (str(i) + "th time with value: " + str(value))
        #     finalHeu = finalHeu + value

        # #print ("final heauristic value: " + str(finalHeu))
        #state_tuple = tuple(item for row in self.init_state for item in row)
        #for i in range(0, maxrange):
        #     (xInit, yInit) = self.getTuple(state, i)
        #     (xFinal, yFinal) = self.getTuple(self.goal_state, i)

        #     currPos = 

        for row in range(0, self.n):
            for col in range(0, self.n):
                currNumInPos = state[row][col]
                indexOfNum = row * self.n + col
                # actualIndexInGoal = self.getGoalPos(currNumInPos)

                eucliValue = self.euclidDist[indexOfNum][currNumInPos]

                finalHeu = finalHeu + eucliValue

        return finalHeu 

    def solve(self):
        #TODO
        # implement your search algorithm here
        start_time = time.time()
        if not self.isSolvable():
            #self.time = time.time() - start_time
            return ["UNSOLVABLE"]

        frontier = [] 
        # tuple with the following (custom sort func, prev_state, curr_state, listofsteps)
        heapq.heappush(frontier, (self.euclideanHeu(self.init_state), None, self.init_state, []))

        while frontier:
            #print("goes into loop")
            currNode = heapq.heappop(frontier)
            accumulatedHeuValue = currNode[0]
            prevState = currNode[1]
            currState = currNode[2]
            actionList = currNode[3]
            #print("current euclideanHeu is:" + str(currNode[0]))

            if currNode[0] == 0 :
                self.time = time.time() - start_time
                return actionList

            possibleMoves = self.possibleMoves(currState)

            for move in possibleMoves:
                nextState = move[0]
                moveString = move[1]
                tempHeuValue = self.euclideanHeu(nextState)

                tempActionList = copy(actionList)
                tempActionList.append(moveString)

                if tempHeuValue == 0:
                    self.time = time.time() - start_time
                    return tempActionList

                # don't waste time by going back to the previous state
                if nextState != prevState:
                    #print (nextState)
                    heapq.heappush(frontier, (tempHeuValue + len(tempActionList), currState, nextState, tempActionList))
                    self.numNodesGen = self.numNodesGen + 1
                    self.maxNumNodesInQ = max(self.maxNumNodesInQ, len(frontier))
                            

        #return ["LEFT", "RIGHT"] # sample output 

    def possibleMoves(self, curr_state):
        possible_moves = []
                
        zeroValue = self.getTuple(curr_state, 0)

        i = zeroValue[0]
        j = zeroValue[1]
        # move blank up
        up_state = deepcopy(curr_state)
        if i != 0:
            temp = up_state[i-1][j]
            up_state[i-1][j] = up_state[i][j]
            up_state[i][j] = temp  # tile has been moved down
            possible_moves.append([up_state, 'DOWN'])

        # move blank down
        down_state = deepcopy(curr_state)
        if i != len(curr_state)-1:
            temp = down_state[i+1][j]
            down_state[i+1][j] = down_state[i][j]
            down_state[i][j] = temp # tile has been moved up
            possible_moves.append([down_state, 'UP'])

        # move blank left
        left_state = deepcopy(curr_state)
        if j != 0:
            temp = left_state[i][j-1]
            left_state[i][j-1] = left_state[i][j]
            left_state[i][j] = temp # tile has been moved right
            possible_moves.append([left_state, 'RIGHT'])

                # move blank right
        right_state = deepcopy(curr_state)
        if j != len(curr_state)-1:
            temp = right_state[i][j+1]
            right_state[i][j+1] = right_state[i][j]
            right_state[i][j] = temp # tile has been moved left
            possible_moves.append([right_state, 'LEFT'])

        return possible_moves

    # you may add more functions if you think is useful
    def checkActions(self, actionList):
      state = deepcopy(self.init_state)
      for action in actionList:
        (x,y) = self.getTuple(state, 0)
        if (action == "UP"):
          # move the bottom cell upwards =
          state[x][y]= state[x+1][y]
          state[x+1][y]=0
        elif (action == "DOWN"):
          # move the top cell downwards 
          state[x][y]=state[x-1][y]
          state[x-1][y]=0
        elif (action == "LEFT"):
          # move the right cell leftwards
          state[x][y] = state[x][y+1]
          state[x][y+1] = 0
        elif (action == "RIGHT"):
          #move the left cell rightwards 
          state[x][y]=state[x][y-1]
          state[x][y-1]=0
      return state == self.goal_state

    def isSolvable(self):
        numInvert = self.getNumOfInversions()
        if self.n % 2 == 1:
            return (numInvert % 2 == 0)
        else:
            blank = self.getBlank(self.init_tuple)
            blankX=blank//self.n
            blankY=blank%self.n
            return (blankX % 2)!=(numInvert % 2)
    
    def getNumOfInversions(self):
        init_state_tuple = tuple(col for row in self.init_state for col in row)
        invCount = 0
        for i in range(len(init_state_tuple)):
            for j in range(i+1, len(init_state_tuple)):
                if (init_state_tuple[j] > 0 and init_state_tuple[i] > init_state_tuple[j]): 
                    invCount += 1
        return invCount

if __name__ == "__main__":
    # do NOT modify below

    # argv[0] represents the name of the file that is being executed
    # argv[1] represents name of input file
    # argv[2] represents name of destination output file
    if len(sys.argv) != 3:
        raise ValueError("Wrong number of arguments!")

    try:
        f = open(sys.argv[1], 'r')
    except IOError:
        raise IOError("Input file not found!")

    lines = f.readlines()
    
    # n = num rows in input file
    n = len(lines)
    # max_num = n to the power of 2 - 1
    max_num = n ** 2 - 1

    # Instantiate a 2D list of size n x n
    init_state = [[0 for i in range(n)] for j in range(n)]
    goal_state = [[0 for i in range(n)] for j in range(n)]
    

    i,j = 0, 0
    for line in lines:
        for number in line.split(" "):
            if number == '':
                continue
            value = int(number , base = 10)
            if  0 <= value <= max_num:
                init_state[i][j] = value
                j += 1
                if j == n:
                    i += 1
                    j = 0

    for i in range(1, max_num + 1):
        goal_state[(i-1)//n][(i-1)%n] = i
    goal_state[n - 1][n - 1] = 0

    puzzle = Puzzle(init_state, goal_state)
    ans = puzzle.solve()

    if (puzzle.checkActions(ans)):
        print ("0k")
    else:
        print ("damn shit")

    with open(sys.argv[2], 'a') as f:
        for answer in ans:
            f.write(answer+'\n')







