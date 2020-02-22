import os
import sys
import heapq
from copy import copy, deepcopy


class Puzzle(object):
    def __init__(self, init_state, goal_state):
        # you may add more attributes if you think is useful
        self.init_state = init_state
        self.goal_state = goal_state
        self.actions = list()

    def solve(self):
        if not self.is_solvable():
            return ["UNSOLVABLE"]
        
        frontier = []  # contains tuples of (f, prev_state, curr_state, steps)
        heapq.heappush(frontier, (0, None, self.init_state, []))  # first step
        
        while frontier:
            # helper to calculate heuristic of current state
            def calc_heur(curr_state):
                misplaced_tile = 0
                for i in range(len(curr_state)):
                    for j in range(len(curr_state)):
                        if curr_state[i][j] != self.goal_state[i][j]:
                            misplaced_tile += 1
                return misplaced_tile

            # helper to generate the possible moves
            def generate_moves(curr_state):
                possible_moves = []
                
                # find where the space is
                for i in range(len(curr_state)):
                    for j in range(len(curr_state)):
                        if curr_state[i][j] == 0:
                            space_loc = (i, j)
                            break
                
                i = space_loc[0]
                j = space_loc[1]

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
            
            node = heapq.heappop(frontier)
            curr_f = node[0]
            prev_state = node[1]
            curr_state = node[2]

            # goal check, in this case if misplaced tile is zero can stop
            if calc_heur(curr_state) == 0:
                return node[3]

            # explore all the possible actions
            possible_moves = generate_moves(curr_state)

            for move in possible_moves:
                next_state = move[0]
                h = calc_heur(next_state)
                
                next_action = move[1]
                curr_actions = node[3]
                action_list = copy(curr_actions)
                action_list.append(next_action)
                
                # don't waste time by going back to the previous state
                if next_state != prev_state:
                    heapq.heappush(frontier, (len(action_list) + h, curr_state, next_state, action_list))
                    
                if h == 0:
                    node = heapq.heappop(frontier)
                    return node[3]
            
        return node[3]

    # you may add more functions if you think is useful
    def is_solvable(self):
        return self.get_no_of_inv() % 2 == 0

    def get_no_of_inv(self):
        lst_inv = []
        
        # create the string of interest for comparison
        for row in range(len(self.init_state)):
            for col in range(len(self.init_state)):
                lst_inv.append(self.init_state[row][col])
                
        # start counting the inversions
        count = 0
        for i in range(len(lst_inv)):
            for j in range(i + 1, len(lst_inv)):
                if (lst_inv[j] > 0 and lst_inv[i] > lst_inv[j]):
                    count += 1
                    
        return count
    

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







