import os
import sys
import heapq # priority queue
import copy

class Puzzle(object):
    def __init__(self, init_state, goal_state):
        # you may add more attributes if you think is useful
        self.init_state = init_state
        self.goal_state = goal_state
        self.direction = [(1, 0), (-1, 0), (0, -1), (0, 1)]
        self.actionName = ["UP", "DOWN", "RIGHT", "LEFT"]
        self.prev = dict()

        self.n = len(init_state)
        self.initStateString = list()

    def getBlank(self, state):
        for i in range(self.n):
            for j in range(self.n):
                if state[i][j] == 0:
                    return (i, j)

    def isValid(self, i, j):
        return i >= 0 and i < self.n and j >= 0 and j < self.n

    def numToPair(self, num):
        return (num/n, num%n)

    def pairToNum(self, p):
        return p[0]*n+p[1]

    # num of incorrect number
    def heuristic(self, state):
        num = 0
        for i in range(self.n):
            for j in range(self.n):
                if state[i][j] != self.goal_state[i][j]:
                    num += 1
        return num

    def getActions(self):
        state = tuple(item for row in self.goal_state for item in row)
        (blankX, blankY) = self.getBlank(self.goal_state)
        actionList=[]
        while self.prev[state] != -1:
            action = self.prev[state]
            actionList.append(self.actionName[action])
            (prevX, prevY) = (blankX - self.direction[action][0], blankY - self.direction[action][1])
            prevState = list(state)
            prevState[self.pairToNum((prevX, prevY))]=0
            prevState[self.pairToNum((blankX,blankY))]=state[self.pairToNum((prevX, prevY))]
            state = tuple(prevState)
            blankX = prevX
            blankY = prevY

        actionList.reverse()
        if not self.checkActions(actionList):
          print("Wrong")
        return actionList
    
    def checkActions(self, actionList):
        state = copy.deepcopy(self.init_state)
        for action in actionList:
            (x,y) = self.getBlank(state)
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

    def generateChildren(self, state):
        children = []
        blank = self.getBlank(state)
        for i in range(4):
            x = blank[0] + self.direction[i][0]
            y = blank[1] + self.direction[i][1]
            if not self.isValid(x, y):
                continue
            new_state = copy.deepcopy(state)
            new_state[x][y], new_state[blank[0]][blank[1]] = new_state[blank[0]][blank[1]], new_state[x][y]
            
            children.append((i, new_state))
        return children


    def solve(self):
        #TODO
        # implement your search algorithm here

        if not self.isSolvable():
            return ["UNSOLVABLE"]
        frontier = []  # priority queue

        goal_tuple = tuple(item for row in self.goal_state for item in row)
        init_tuple = tuple(item for row in self.init_state for item in row)
        frontier.append((self.heuristic(init_state), init_state))

        self.prev[init_tuple]=-1
        heapq.heapify(frontier)

        while len(frontier) > 0:
            node = heapq.heappop(frontier)

            children = self.generateChildren(node[1])
            for child in children:
                stateTuple=tuple(item for row in child[1] for item in row)
                if self.prev.get(stateTuple) is not None:
                    continue

                self.prev[stateTuple]=child[0]
                if child[1] == self.goal_state:
                    return self.getActions()
                heapq.heappush(frontier, (self.heuristic(child[1]),child[1]))

        return ["UNSOLVABLE"] # sample output

    # you may add more functions if you think is useful

    def isSolvable(self):
        numInvert = self.getNumOfInversions()
        if n % 2 == 1:
            return (numInvert % 2 == 0)
        else:
            (blankX, blankY) = self.getBlank(init_state)
            return (blankX % 2)!=(numInvert % 2)
    
    def getNumOfInversions(self):
        # create the string of interest for comparison 
        for row in range(len(init_state)):
            for col in range(len(init_state)):
                self.initStateString.append(self.init_state[row][col])
        # start counting the inversions. 
        invCount = 0
        for i in range(len(self.initStateString)):
            for j in range(i+1, len(self.initStateString)):
                if (self.initStateString[j] > 0 and self.initStateString[i] > self.initStateString[j]): 
                    invCount += 1
        return invCount

    def getNumOfInversions(self):
        # create the string of interest for comparison
        for row in range(len(init_state)):
            for col in range(len(init_state)):
                self.initStateString.append(self.init_state[row][col]);
        # start counting the inversions.
        invCount = 0
        for i in range(len(self.initStateString)):
            for j in range(i + 1, len(self.initStateString)):
                if (self.initStateString[j] > 0 and self.initStateString[i] > self.initStateString[j]):
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

    with open(sys.argv[2], 'a') as f:
        for answer in ans:
            f.write(answer+'\n')







