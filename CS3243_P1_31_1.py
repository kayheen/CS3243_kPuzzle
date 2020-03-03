import os
import sys
import copy
import time 

from collections import deque

class Puzzle(object):

    def __init__(self, init_state, goal_state):
        # you may add more attributes if you think is useful
        self.init_state = init_state
        self.goal_state = goal_state
        self.actions = [(1,0),(-1,0),(0,-1),(0,1)]
        self.actionName = ["UP", "DOWN", "RIGHT", "LEFT"]
        self.initStateString = list()

        self.n = len(init_state)
        self.size = self.n*self.n
        self.visited = dict()

        self.numNodesGen = 0
        self.maxNumNodesInQ = 0
        self.time = 0

    #this method gets the position of the blank state 
    def getBlank(self, state):
        for i in range(self.n):
            for j in range(self.n):
                if state[i][j]==0:
                    return (i,j)

    def numToPair(self, num):
        return (num/self.n, num%self.n)

    # converts a tuple ie a coordinate into the corresponding number in the tuple
    def pairToNum(self, p):
        return p[0]*self.n+p[1]

    # checks if the current position is within the n*n tile
    def isValid(self, i, j):
        return i>=0 and i<self.n and j>=0 and j<self.n

    def getActions(self):
        state = tuple(item for row in self.goal_state for item in row)
        (blankX, blankY) = self.getBlank(self.goal_state)
        actionList=[]
        while self.visited[state] != -1:

            action = self.visited[state]
            actionList.append(self.actionName[action])
            (prevX, prevY) = (blankX - self.actions[action][0], blankY - self.actions[action][1])
            prevState = list(state)
            prevState[self.pairToNum((prevX, prevY))]=0
            prevState[self.pairToNum((blankX,blankY))]=state[self.pairToNum((prevX, prevY))]
            state = tuple(prevState)
            blankX = prevX
            blankY = prevY

        actionList.reverse()
        #if not self.checkActions(actionList):
          #print("Wrong")
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

    def bfs(self):
        queue = deque()
        goal_tuple = tuple(item for row in self.goal_state for item in row)
        init_tuple = tuple(item for row in self.init_state for item in row)
        self.visited[init_tuple]=-1
        queue.append((init_tuple, 0, self.getBlank(self.init_state)))
        # major bfs queue 
        while queue:
            head = queue.popleft()
            state= head[0]
            (x, y) = head[2]
            step = head[1] 
            # looks through the 4 different options that the tiles around can move to this blank space
            for i in range(4):
            		# choosing the next tile to move
                (nextX, nextY) = (x + self.actions[i][0], y + self.actions[i][1])

                # if not a valid movement, then try another state
                if not self.isValid(nextX, nextY):
                    continue

                # a valid movement.
                nextState = list(state)
                nextState[self.pairToNum((nextX, nextY))]=0
                nextState[self.pairToNum((x,y))]=state[self.pairToNum((nextX, nextY))]
                nextState = tuple(nextState)

                # if the state has been visited already, then try another state
                if not self.visited.get(nextState) is None:
                    continue
                # else set the next state to visited (and also add the current movement to it) 
                self.visited[nextState] = i
                if nextState == goal_tuple:
                    queue.clear()
                    return self.getActions()
                # add this next state to the queue. 
                queue.append((nextState, step+1, (nextX, nextY)))
                self.numNodesGen = self.numNodesGen + 1
                #print (self.numNodesGen)
                self.maxNumNodesInQ = max(self.maxNumNodesInQ, len(queue))
        
        return ['UNSOLVABLE']
        

    def isSolvable(self):
        numInvert = self.getNumOfInversions()
        if self.n % 2 == 1:
            return (numInvert % 2 == 0)
        else:
            (blankX, blankY) = self.getBlank(self.init_state)
            return (blankX % 2)!=(numInvert % 2)
    
    def getNumOfInversions(self):
        # create the string of interest for comparison 
        for row in range(len(self.init_state)):
            for col in range(len(self.init_state)):
                self.initStateString.append(self.init_state[row][col]);
        # start counting the inversions. 
        invCount = 0;
        for i in range(len(self.initStateString)):
            for j in range(i+1, len(self.initStateString)):
                if (self.initStateString[j] > 0 and self.initStateString[i] > self.initStateString[j]): 
                    invCount += 1;
        return invCount;

    def solve(self):
        #TODO
        # implement your search algorithm here
        start = time.time()
        if (self.isSolvable()):
          #then call BFS 
          actions = self.bfs();
          self.time = time.time() - start
          return actions
        else:
          return ["UNSOLVABLE"]

    # you may add more functions if you think is useful

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