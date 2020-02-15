import os
import sys
import heapq # priority queue
import copy

direction = [(1, 0), (-1, 0), (0, -1), (0, 1)]
actionName = ["UP", "DOWN", "RIGHT", "LEFT"]

class Puzzle(object):
    def __init__(self, init_state, goal_state):
        # you may add more attributes if you think is useful
        self.init_state = init_state
        self.goal_state = goal_state

        self.n = len(init_state)

        self.g = 0
        self.h = self.heuristic()
        self.f = self.g + self.h

        self.hash_value = hash(str(self.init_state))

        self.parent = None
        self.action = None
        self.initStateString = list()


    def __lt__(self, other):
        return self.f < other.f

    def __eq__(self, other):
        return self.hash_value == other.hash_value

    def getBlank(self, state):
        for i in range(self.n):
            for j in range(self.n):
                if state[i][j] == 0:
                    return (i, j)

    def isValid(self, i, j):
        return i >= 0 and i < self.n and j >= 0 and j < self.n

    # num of incorrect number
    def heuristic(self):
        num = 0
        for i in range(self.n):
            for j in range(self.n):
                if self.init_state[i][j] != self.goal_state[i][j]:
                    num += 1
        return num

    def generateChildren(self):
        children = []
        blank = self.getBlank(self.init_state)
        for i in range(4):
            x = blank[0] + direction[i][0]
            y = blank[1] + direction[i][1]
            if self.isValid(x, y):
                new_state = copy.deepcopy(self.init_state)
                new_state[x][y], new_state[blank[0]][blank[1]] = new_state[blank[0]][blank[1]], new_state[x][y]
                child_node = Puzzle(new_state, self.goal_state)
                child_node.g = self.g + 1
                child_node.parent = self
                child_node.action = actionName[i]
                children.append(child_node)
        return children

    def isGoal(self):
        return hash(str(self.init_state)) == hash(str(self.goal_state))

    def solve(self):
        #TODO
        # implement your search algorithm here

        path = []

        frontier = []  # priority queue
        explored_set = set()  # hashset of explored nodes' hash_value

        frontier.append(self)
        heapq.heapify(frontier)

        while len(frontier) > 0:
            node = heapq.heappop(frontier)

            if node.hash_value in explored_set:
                continue

            if not node.isSolvable():
                continue

            explored_set.add(node.hash_value)

            if node.isGoal():
                while node.parent:
                    path.append(node.action)
                    node = node.parent
                path.reverse()
                return path

            children = node.generateChildren()
            for child in children:
                heapq.heappush(frontier, child)

        return ["UNSOLVABLE"] # sample output

    # you may add more functions if you think is useful

    def isSolvable(self):
        numInvert = self.getNumOfInversions();
        return (numInvert % 2 == 0)

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







