import os
import sys
import CS3243_P1_31_1 as Case1
import CS3243_P1_31_2 as Case2
import CS3243_P1_31_3 as Case3
import CS3243_P1_31_4 as Case4

def printResults(ans, num):
    print (str(num) + " -> Total Number of Nodes Generated: " + str(ans.numNodesGen))
    print (str(num) + " -> Max Number of Nodes Generated: " + str(ans.maxNumNodesInQ))
    print (str(num) + " -> Time taken: " + str(ans.time))
    print (" ")

def initArray(lines, init_state, goal_state):
    # n = num rows in input file
    n = len(lines)
    # max_num = n to the power of 2 - 1
    max_num = n ** 2 - 1

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

if __name__ == "__main__":
    #argv[0] represents the name of the file that is being executed
    #argv[1] represents name of input file
    #argv[2] represents name of destination output file
    if len(sys.argv) != 3:
        raise ValueError("Wrong number of arguments!")

    try:
        f = open(sys.argv[1], 'r')
    except IOError:
        raise IOError("Input file not found!")

    lines = f.readlines()

    # n = num rows in input file
    n = len(lines) 

    # Instantiate a 1st 2D list of size n x n
    init_state1 = [[0 for i in range(n)] for j in range(n)]
    goal_state1 = [[0 for i in range(n)] for j in range(n)]
    
    initArray(lines, init_state1, goal_state1)

    # Instantiate a 2nd 2D list of size n x n
    init_state2 = [[0 for i in range(n)] for j in range(n)]
    goal_state2 = [[0 for i in range(n)] for j in range(n)]

    initArray(lines, init_state2, goal_state2)

    # Instantiate a 3rd 2D list of size n x n
    init_state3 = [[0 for i in range(n)] for j in range(n)]
    goal_state3 = [[0 for i in range(n)] for j in range(n)]

    initArray(lines, init_state3, goal_state3)

    # Instantiate a 4th 2D list of size n x n
    init_state4 = [[0 for i in range(n)] for j in range(n)]
    goal_state4 = [[0 for i in range(n)] for j in range(n)]

    initArray(lines, init_state4, goal_state4)

    puzzle1 = Case1.Puzzle(init_state1, goal_state1)
    puzzle2 = Case2.Puzzle(init_state2, goal_state2)
    puzzle3 = Case3.Puzzle(init_state3, goal_state3)
    puzzle4 = Case4.Puzzle(init_state4, goal_state4)
    
    ans1 = puzzle1.solve()
    ans2 = puzzle2.solve()
    ans3 = puzzle3.solve()
    ans4 = puzzle4.solve()

    printResults(puzzle1, 1)
    #printResults(puzzle2, 2)
    #printResults(puzzle3, 3)
    #printResults(puzzle4, 4)

    with open(sys.argv[2], 'a') as f:
        for answer in ans1:
            f.write(answer+'\n')


# class Puzzle(object):
#     def __init__(self, init_state, goal_state):
#         # you may add more attributes if you think is useful
#         self.init_state = init_state
#         self.goal_state = goal_state
#         self.actions = list()

#     def solve(self):
#         #TODO
#         # implement your search algorithm here
        
#         return ["LEFT", "RIGHT"] # sample output 

#     # you may add more functions if you think is useful

# if __name__ == "__main__":
#     # do NOT modify below

#     # argv[0] represents the name of the file that is being executed
#     # argv[1] represents name of input file
#     # argv[2] represents name of destination output file
#     if len(sys.argv) != 3:
#         raise ValueError("Wrong number of arguments!")

#     try:
#         f = open(sys.argv[1], 'r')
#     except IOError:
#         raise IOError("Input file not found!")

#     lines = f.readlines()
    
#     # n = num rows in input file
#     n = len(lines)
#     # max_num = n to the power of 2 - 1
#     max_num = n ** 2 - 1

#     # Instantiate a 2D list of size n x n
#     init_state = [[0 for i in range(n)] for j in range(n)]
#     goal_state = [[0 for i in range(n)] for j in range(n)]
    

#     i,j = 0, 0
#     for line in lines:
#         for number in line.split(" "):
#             if number == '':
#                 continue
#             value = int(number , base = 10)
#             if  0 <= value <= max_num:
#                 init_state[i][j] = value
#                 j += 1
#                 if j == n:
#                     i += 1
#                     j = 0

#     for i in range(1, max_num + 1):
#         goal_state[(i-1)//n][(i-1)%n] = i
#     goal_state[n - 1][n - 1] = 0

#     puzzle = Puzzle(init_state, goal_state)
#     ans = puzzle.solve()

#     with open(sys.argv[2], 'a') as f:
#         for answer in ans:
#             f.write(answer+'\n')







