import os
import sys
import CS3243_P1_31_1 as Case1
import CS3243_P1_31_2 as Case2
import CS3243_P1_31_3 as Case3
import CS3243_P1_31_4 as Case4
import random 
import copy 

def initArray(lines, n, init_state, goal_state):
    max_num = n ** 2 - 1

    for i in range (0, n):
        for j in range(0, n):
            init_state[i][j] = lines[i*n + j]


    for i in range(1, max_num + 1):
        goal_state[(i-1)//n][(i-1)%n] = i
    goal_state[n - 1][n - 1] = 0

def callRelevantMethods(lines):
    n = 3
    # Instantiate a 2D list of size n x n
    init_state1 = [[0 for i in range(n)] for j in range(n)]
    goal_state1 = [[0 for i in range(n)] for j in range(n)]
    
    initArray(lines, n, init_state1, goal_state1)

    puzzle1 = Case1.Puzzle(init_state1, goal_state1)
    puzzle2 = Case2.Puzzle(init_state1, goal_state1)
    puzzle3 = Case3.Puzzle(init_state1, goal_state1)
    puzzle4 = Case4.Puzzle(init_state1, goal_state1)
    
    ans1 = puzzle1.solve()
    ans2 = puzzle2.solve()
    ans3 = puzzle3.solve()
    ans4 = puzzle4.solve()

    print ("Uninformed Search BFS returns: " + str(ans1))
    print ("Informed Search Misplacement returns: " + str(ans2))
    print ("Informed Search Manhatten returns: " + str(ans3))
    print ("Informed Search Euclidean returns: " + str(ans4))

    if ans1 != ['UNSOLVABLE']:
        return len(ans1) == len(ans2) and len(ans2) == len(ans3) and len(ans3) == len(ans4) and checkActions(init_state1, goal_state1, ans1, 3) and checkActions(init_state1, goal_state1, ans2, 3) and checkActions(init_state1, goal_state1, ans3, 3) and checkActions(init_state1, goal_state1, ans4, 3)
    else: 
        return len(ans1) == len(ans2) and len(ans2) == len(ans3) and len(ans3) == len(ans4)

def getBlank(state, n):
    for i in range(n):
        for j in range(n):
            if state[i][j]==0:
                return (i,j)

def checkActions(init_state, goal_state, actionList, n):
    state = copy.deepcopy(init_state)
    for action in actionList:
        (x,y) = getBlank(state, n)
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
    return state == goal_state

if __name__ == "__main__":

    # Test 1: Checking for correctness and optimality of solutions for all 4 implementations
    successCount = 0

    random.seed(6)
    list3 = [0, 1, 2, 3, 4, 5, 6, 7, 8]

    failCase = []
    failList = []

    
    for i in range(1, 101):
        print ("====== Test Case " + str(i) + " for n = 3 ======")
        random.shuffle(list3)
        print(list3)

        if callRelevantMethods(list3):
            print ("Success! All the 4 heuristics return an optimal solution.")
            print(" ")
            successCount = successCount + 1
        else:
            print("Failed")
            print(" ")
            failCase.append(i)
            failList.append(copy.deepcopy(list3))
 
    print("====== Case Summary of the Correctness of the Solutions for Each 4 Cases in Each Test ======")
    print("A total of " + str(successCount) + " successes out of 100 cases.")
    print("A total of " + str(100 - successCount) + " failures.")
    print ("Cases failed: " + str(failCase))
    print("Corresponding list: " + str(failList))
    print(" ")

    #Test 2: Comparing the time taken for each algorithm (heuristic) to solve a fixed set of puzzles 
    puzzle_3a = [1, 8, 2, 0, 4, 3, 7, 6, 5]
    puzzle_3b = [8, 6, 7, 2, 5, 4, 3, 0, 1]
    puzzle_3c = [8, 7, 4, 0, 6, 5, 2, 1, 3]

    puzzle_4a = [1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 0, 12, 9, 13, 14, 15]
    puzzle_4b = [2, 1, 4, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0]
    puzzle_4c = [1, 2, 3, 4, 6, 5, 8, 7, 9, 10, 11, 12, 13, 14, 15, 0]


    puzzle_5a = [1, 3, 4, 10, 5, 7, 2, 8, 0, 14, 6, 11, 12, 9, 15, 16, 17, 13, 18, 19, 21, 22, 23, 24, 20]
    puzzle_5b = [1, 3, 4, 10, 5, 7, 2, 12, 8, 14, 6, 11, 13, 15, 0, 17, 23, 18, 9, 19, 16, 21, 22, 24, 20]
    puzzle_5c = [1, 3, 4, 0, 10, 7, 2, 12, 8, 5, 6, 11, 13, 15, 14, 17, 23, 18, 9, 19, 16, 21, 22, 24, 20]
    
    puzzleList = [puzzle_3a, puzzle_3b, puzzle_3c, puzzle_4a, puzzle_4b, puzzle_4c, puzzle_5a, puzzle_5b, puzzle_5c]
    puzzleN = [3, 3, 3, 4, 4, 4, 5, 5, 5]
    count = 0 
    for puzzle in puzzleList:
        n = puzzleN[count]

        print ("====== Testing for n = " + str(n) + " Case " + str(count%3) + " with puzzle sequence: " + str(puzzle) + " ======")

        totalHamming = 0
        totalManhattan = 0
        totalEuclidean = 0 

        numNodesHamming = 0
        numNodesManhattan = 0
        numNodesEuclidean = 0 

        maxNumNodesInQHamming = 0
        maxNumNodesInQManhattan = 0
        maxNumNodesInQEuclidean = 0 
        

        # Instantiate a 2D list of size n x n
        init_state = [[0 for i in range(n)] for j in range(n)]
        goal_state = [[0 for i in range(n)] for j in range(n)]
        initArray(puzzle, n, init_state, goal_state)

        for i in range(50):
            #puzzle1 = Case1.Puzzle(init_state1, goal_state1)
            puzzle2 = Case2.Puzzle(init_state, goal_state)
            puzzle3 = Case3.Puzzle(init_state, goal_state)
            puzzle4 = Case4.Puzzle(init_state, goal_state)
    
            #ans1 = puzzle1.solve()
            ans2 = puzzle2.solve()
            totalHamming = totalHamming + puzzle2.time 

            ans3 = puzzle3.solve()
            totalManhattan = totalManhattan + puzzle3.time

            ans4 = puzzle4.solve()
            totalEuclidean = totalEuclidean + puzzle4.time 

            if i == 0:
                numNodesHamming = puzzle2.numNodesGen
                numNodesManhattan = puzzle3.numNodesGen
                numNodesEuclidean = puzzle4.numNodesGen

                maxNumNodesInQHamming = puzzle2.maxNumNodesInQ
                maxNumNodesInQManhattan = puzzle3.maxNumNodesInQ
                maxNumNodesInQEuclidean = puzzle4.maxNumNodesInQ

        avgTimeHamming = totalHamming / 50
        avgTimeManhattan = totalManhattan / 50
        avgTimeEuclidean = totalEuclidean / 50 

        #print appropriate results 
        print(" ")
        print("Results for n = " + str(puzzleN[count]) + " Case " + str(count%3) + ":")
        print(" ")

        print("Average Time Taken For: ")
        print("[Hammings]: " + str(avgTimeHamming))
        print("[Manhattan]: "  + str(avgTimeManhattan))
        print("[Euclidean]: " + str(avgTimeEuclidean))
        print("============")

        print("Total Number of Nodes Explored: ")
        print("[Hammings]: " + str(numNodesHamming))
        print("[Manhattan]: " + str(numNodesManhattan))
        print("[Euclidean]: " + str(numNodesEuclidean))
        print("============")

        print("Max Number of Nodes in Frontier: ")
        print("[Hammings]: " + str(maxNumNodesInQHamming))
        print("[Manhattan]: " + str(maxNumNodesInQManhattan))
        print("[Euclidean]: " + str(maxNumNodesInQEuclidean))
        print("========================")
        print(" ")

        count = count + 1
