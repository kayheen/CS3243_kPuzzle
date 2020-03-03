import os
import sys
import heapq # priority queue
import copy
import time

# h2: manhattan distance

class Puzzle(object):
    def __init__(self, init_state, goal_state):
        # you may add more attributes if you think is useful
        self.init_state = init_state
        self.goal_state = goal_state
        self.n = len(init_state)
        self.init_tuple = tuple(item for row in self.init_state for item in row)
        self.goal_tuple = tuple(item for row in self.goal_state for item in row)
        self.pos = [0 for i in self.goal_tuple]
        
        for i in range(len(self.goal_tuple)):
            self.pos[self.goal_tuple[i]] = i
        self.manhattanDist = [[0 for i in self.goal_tuple] for j in self.goal_tuple]
        
        for i in range(len(self.goal_tuple)):
            for j in range(len(self.goal_tuple)):
                self.manhattanDist[i][j] = abs(i//self.n-j//self.n) + abs(i%self.n - j%self.n)
            
        self.direction = [(1, 0), (0, -1), (-1, 0), (0, 1)]
        self.actionNames = ["UP",  "RIGHT", "DOWN", "LEFT"]
        
        self.prev = dict()
        self.cost = dict()

        self.numNodesGen = 0
        self.maxNumNodesInQ = 0
        self.time = 0

    def getBlank(self, state_tuple):
        return state_tuple.index(0)

    # manhattan distance
    def heuristic(self, state):
        sumDist = 0
        for i in range(len(state)):         
            if state[i]!=0:
                sumDist+=self.manhattanDist[i][self.pos[state[i]]]
        return sumDist

    def getActions(self):
        state = tuple(item for row in self.goal_state for item in row)
        blank = self.getBlank(self.goal_tuple)
        blankX=blank//self.n
        blankY=blank%self.n
        actionList=[]
        while self.prev[state] != -1:
            action = self.prev[state]
            actionList.append(self.actionNames[action])
            (prevX, prevY) = (blankX - self.direction[action][0], blankY - self.direction[action][1])
            prevState = list(state)
            prevState[prevX*self.n+prevY]=0
            prevState[blankX*self.n+blankY]=state[prevX*self.n+prevY]
            state = tuple(prevState)
            blankX = prevX
            blankY = prevY

        actionList.reverse()
        if not self.checkActions(actionList):
            print("Wrong")
        return actionList
    
    def checkActions(self, actionList):
        state = list(self.init_tuple)
        for action in actionList:
            blank = self.getBlank(state)
            if (action == "UP"):
                # move the bottom cell upwards
                state[blank]= state[blank+self.n]
                state[blank+self.n]=0
            elif (action == "DOWN"):
                # move the top cell downwards 
                state[blank]=state[blank-self.n]
                state[blank-self.n]=0
            elif (action == "LEFT"):
                # move the right cell leftwards
                state[blank] = state[blank+1]
                state[blank+1] = 0
            elif (action == "RIGHT"):
                #move the left cell rightwards 
                state[blank]=state[blank-1]
                state[blank-1]=0
        return tuple(state) == self.goal_tuple

    def solve(self):
        #TODO
        # implement your search algorithm here

        start_time = time.time()
        if not self.isSolvable():
            return ["UNSOLVABLE"]
        
        frontier = []  # priority queue

        frontier.append((self.heuristic(self.init_tuple), self.init_tuple, self.getBlank(self.init_tuple)))

        self.prev[self.init_tuple]=-1
        self.cost[self.init_tuple]=0
        heapq.heapify(frontier)

        while frontier:
            node = heapq.heappop(frontier)
            
            cur_f = node[0]
            cur_state = node[1]
            cur_heuristic = self.heuristic(cur_state)
            cur_cost = cur_f - cur_heuristic
            blank = node[2]
            
            if cur_state == self.goal_tuple:
                answer = self.getActions()
                self.time = time.time() - start_time
                print(self.time)
                return answer

            if cur_cost>self.cost[cur_state]:
                continue
            
            blankX = blank//self.n
            blankY = blank%self.n
            for i in range(4):
                x = blankX + self.direction[i][0]
                y = blankY + self.direction[i][1]
                if not (x >= 0 and x < self.n and y >= 0 and y < self.n):
                    continue
                new_state = list(cur_state)
                new_blank = x*self.n+y
                new_state[new_blank]=0
                new_state[blank]=cur_state[new_blank]
                new_heuristic = cur_heuristic
                
                destination = self.pos[cur_state[new_blank]]
                new_heuristic-=self.manhattanDist[new_blank][destination]
                new_heuristic+=self.manhattanDist[blank][destination]
                
                new_state=tuple(new_state)
            
                if self.cost.get(new_state) is not None and self.cost[new_state] <= cur_cost + 1:
                   continue
                
                self.cost[new_state] = cur_cost + 1
                
                self.prev[new_state] = i
                heapq.heappush(frontier, (new_heuristic+cur_cost+1,new_state,new_blank))
                self.numNodesGen = self.numNodesGen + 1
                self.maxNumNodesInQ = max(self.maxNumNodesInQ, len(frontier))

        return ["UNSOLVABLE"] # sample output

    # you may add more functions if you think is useful

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

    with open(sys.argv[2], 'a') as f:
        for answer in ans:
            f.write(answer+'\n')