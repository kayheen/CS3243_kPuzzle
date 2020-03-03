import os
import sys
import CS3243_P1_31_1 as Case1
import CS3243_P1_31_2 as Case2
import CS3243_P1_31_3 as Case3
import CS3243_P1_31_4 as Case4
import random 
import multiprocessing
import time 


def printResults(ans, algo):
    print (algo+ " -> Total Number of Nodes Generated: " + str(ans.numNodesGen))
    print (algo + " -> Max Number of Nodes Generated: " + str(ans.maxNumNodesInQ))
    print (algo + " -> Time taken: " + str(ans.time))
    print (" ")
    compareResults(ans, algo)

def compareResults(ans, algo):
    global minimumNodeGenerated
    global minimumMaxNodeInQ
    global fastestAlgo
    global smallestSpaceAlgo

    minimumNodeGenerated = min(minimumNodeGenerated, ans.numNodesGen)
    minimumMaxNodeInQ = min(minimumMaxNodeInQ, ans.maxNumNodesInQ)

    if (minimumNodeGenerated == ans.numNodesGen and minimumNodeGenerated != 0) :
        fastestAlgo = algo

    if (minimumMaxNodeInQ == ans.maxNumNodesInQ and minimumMaxNodeInQ != 0):
        smallestSpaceAlgo = algo

def printFinalResults():
    global minimumNodeGenerated
    global minimumMaxNodeInQ
    global fastestAlgo
    global smallestSpaceAlgo

    print(" ")
    print("Minimum number of nodes generated: " + str(minimumNodeGenerated))
    print( "Lowest Time Complexity: " + str(fastestAlgo))
    print("Minimum max number of nodes in queue: " + str(minimumMaxNodeInQ))
    print("Lowest Space Complexity: " + str(smallestSpaceAlgo))
    minimumNodeGenerated = 1000000
    minimumMaxNodeInQ = 1000000
    fastestAlgo = "NIL"
    smallestSpaceAlgo = "NIL"
    print("====== End of Test ======")
    print(" ")

def initArray(lines, n, init_state, goal_state):
    # n = num rows in input file
    #n = len(lines)
    # max_num = n to the power of 2 - 1
    max_num = n ** 2 - 1

    # i,j = 0, 0
    # for line in lines:
    #     for number in line.split(" "):
    #         if number == '':
    #             continue
    #         value = int(number , base = 10)
    #         if  0 <= value <= max_num:
    #             init_state[i][j] = value
    #             j += 1
    #             if j == n:
    #                 i += 1
    #                 j = 0

    for i in range (0, n):
        for j in range(0, n):
            init_state[i][j] = lines[i*n + j]


    for i in range(1, max_num + 1):
        goal_state[(i-1)//n][(i-1)%n] = i
    goal_state[n - 1][n - 1] = 0

def callRelevantMethods(lines):
    n = 3
    # Instantiate a 1st 2D list of size n x n
    init_state1 = [[0 for i in range(n)] for j in range(n)]
    goal_state1 = [[0 for i in range(n)] for j in range(n)]
    
    initArray(lines, n, init_state1, goal_state1)

    # Instantiate a 2nd 2D list of size n x n
    init_state2 = [[0 for i in range(n)] for j in range(n)]
    goal_state2 = [[0 for i in range(n)] for j in range(n)]

    initArray(lines, n, init_state2, goal_state2)

    # Instantiate a 3rd 2D list of size n x n
    init_state3 = [[0 for i in range(n)] for j in range(n)]
    goal_state3 = [[0 for i in range(n)] for j in range(n)]

    initArray(lines, n, init_state3, goal_state3)

    # Instantiate a 4th 2D list of size n x n
    init_state4 = [[0 for i in range(n)] for j in range(n)]
    goal_state4 = [[0 for i in range(n)] for j in range(n)]

    initArray(lines, n, init_state4, goal_state4)

    puzzle1 = Case1.Puzzle(init_state1, goal_state1)
    puzzle2 = Case2.Puzzle(init_state2, goal_state2)
    puzzle3 = Case3.Puzzle(init_state3, goal_state3)
    puzzle4 = Case4.Puzzle(init_state4, goal_state4)
    
    ans1 = puzzle1.solve()
    ans2 = puzzle2.solve()
    ans3 = puzzle3.solve()
    ans4 = puzzle4.solve()

    printResults(puzzle1, "UninformedSearch BFS")
    printResults(puzzle2, "InformedSearch Misplacements")
    printResults(puzzle3, "InformedSearch Manhatten Distance")
    printResults(puzzle4, "InformedSearch Euclidean Distance")

    printFinalResults()
    # with open(sys.argv[2], 'a') as f:
    #     for answer in ans1:
    #         f.write(answer+'\n')

def callRelevantMethodsWithN(lines, n):
    #print("got in here")
    # Instantiate a 2nd 2D list of size n x n
    init_state2 = [[0 for i in range(n)] for j in range(n)]
    goal_state2 = [[0 for i in range(n)] for j in range(n)]

    initArray(lines, n, init_state2, goal_state2)

    # Instantiate a 3rd 2D list of size n x n
    init_state3 = [[0 for i in range(n)] for j in range(n)]
    goal_state3 = [[0 for i in range(n)] for j in range(n)]

    initArray(lines, n, init_state3, goal_state3)

    # Instantiate a 4th 2D list of size n x n
    init_state4 = [[0 for i in range(n)] for j in range(n)]
    goal_state4 = [[0 for i in range(n)] for j in range(n)]

    initArray(lines, n, init_state4, goal_state4)

    # puzzle1 = Case1.Puzzle(init_state1, goal_state1)
    puzzle2 = Case2.Puzzle(init_state2, goal_state2)
    puzzle3 = Case3.Puzzle(init_state3, goal_state3)
    puzzle4 = Case4.Puzzle(init_state4, goal_state4)
    
    # ans1 = puzzle1.solve()
    ans2 = puzzle2.solve()
    ans3 = puzzle3.solve()
    ans4 = puzzle4.solve()

    print(ans2)
    # printResults(puzzle1, 1)
    printResults(puzzle2, "InformedSearch Misplacements")
    printResults(puzzle3, "InformedSearch Manhatten Distance")
    printResults(puzzle4, "InformedSearch Euclidean Distance")

    printFinalResults()
    

if __name__ == "__main__":
    global minimumNodeGenerated
    global minimumMaxNodeInQ 
    global fastestAlgo 
    global smallestSpaceAlgo 

    minimumNodeGenerated = 10000000000
    minimumMaxNodeInQ = 1000000000
    fastestAlgo = "NIL"
    smallestSpaceAlgo = "NIL"
    #argv[0] represents the name of the file that is being executed
    #argv[1] represents name of input file
    #argv[2] represents name of destination output file
    # if len(sys.argv) != 3:
    #     raise ValueError("Wrong number of arguments!")

    # try:
    #     f = open(sys.argv[1], 'r')
    # except IOError:
    #     raise IOError("Input file not found!")

    # lines = f.readlines()

    # # n = num rows in input file
    # n = len(lines) 

    random.seed(6)
    list3 = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    list4 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    list5 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]

    for i in range(1, 51):
        print ("====== Test Case " + str(i) + " for n = 3 ======")
        random.shuffle(list3)
        # print(list3)
        #str3 = " ".join(str(j) for j in list3)
        # print(str3)
        callRelevantMethods(list3)
        list3 = [0, 1, 2, 3, 4, 5, 6, 7, 8]

    for i in range (1, 51):
        print ("====== Test Case " + str(i) + " for n = 4 ======")
        random.shuffle(list4)
        #print(list4)
        #str4 = " ".join(str(j) for j in list4)
        # Start foo as a process
        p = multiprocessing.Process(target=callRelevantMethodsWithN, name="callRelevantMethodsWithN", args=(list4, 4,))
        p.start()

        # Wait 10 seconds for foo
        time.sleep(20)

        # Terminate foo
        p.terminate()

        # Cleanup
        p.join()
        #callRelevantMethodsWithN(list4, 4)
        # print(str4)
        list4 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

    for i in range(1, 51):
        print ("====== Test Case " + str(i) + " for n = 5 ======")
        random.shuffle(list5)
        #print(list5)
        #str5 = " ".join(str(j) for j in list5)
        # Start foo as a process
        p = multiprocessing.Process(target=callRelevantMethodsWithN, name="callRelevantMethodsWithN", args=(list5, 5,))
        p.start()

        # Wait 10 seconds for foo
        time.sleep(20)

        # Terminate foo
        p.terminate()

        # Cleanup
        p.join()
        # callRelevantMethodsWithN(list5, 5)
        #print(str5)
        list5 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]


    