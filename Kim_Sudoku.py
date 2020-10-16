import sys
from time import perf_counter
import math
sys.setrecursionlimit(50000)
N, subblock_height, subblock_width, symbol_set = (0, 0, 0, '123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ')
neighbors = dict()
constraint_sets = list()
count = 0


# Changes the size of the board and the symbol set
def global_variables(length):
    global N
    global symbol_set
    global subblock_height
    global subblock_width
    N = int(math.sqrt(length))  # Sets global variable N (square length and width)
    symbol_set = symbol_set[:N]  # Sets symbol set based on N
    root = math.sqrt(N)  # Sets subblock height and width
    if root == int(root):
        subblock_height = subblock_width = int(root)
    else:
        root = int(root)
        while root > 1:
            if N/root == N//root:
                subblock_height = root
                subblock_width = N//root
                return
            root -= 1
        print("Length of input puzzle is not a square")


# Displays the input board state
def display_board(unused_vals):
    string = ""
    char_count = 0
    for square in unused_vals.keys():
        char = unused_vals[square]
        string += char + " "
        char_count += 1
        if char_count == N:
            print(string)
            string = ""
            char_count = 0


# Displays board state as chars
def turn_in_display_board(unused_vals):
    print_string = ""
    for val in unused_vals.values():
        print_string += val
    print(print_string)


# Creates constraints sets and global dict of neighbors (square mapped to all squares
# it effects)
def constraint_creation():
    global neighbors
    global constraint_sets
    for sets in range(3*N):
        constraint_sets.append(set())
    for r in range(N):  # Creates row and column constraint sets
        for c in range(N):
            constraint_sets[r].add(r*N+c)  # Row sets
            constraint_sets[N+r].add(r+c*N)  # Column sets
    for block in range(N):  # Creates block sets #use mod for upper left corner of blocks
        for c in range(subblock_width):
            for r in range(subblock_height):
                constraint_sets[2*N+block].add(block % subblock_height * subblock_width
                                               + block // subblock_height * subblock_height * N +
                                               c+r*N)
    for square in range(N ** 2):  # Creates neighbors dict
        neighbors[square] = set()
        for constraint_set in constraint_sets:
            if square in constraint_set:
                neighbors[square] = neighbors[square].union(constraint_set)
                neighbors[square].remove(square)  # Removes each square from its own neighbors


# Basic check, determines whether end state are plausible
# def check(state):
#     num_in_set = dict()
#     for char in state:
#         if char in symbol_set:
#             if char not in num_in_set.keys():
#                 num_in_set[char] = 0
#             num_in_set[char] += 1
#     print(num_in_set)


# Advanced check, determines whether a solution state works
def advanced_check(unused_vals):
    for constraint_set in constraint_sets:
        for symbol in symbol_set:
            symbol_count = 0
            for neighbor in constraint_set:
                if unused_vals[neighbor] == symbol:
                    symbol_count += 1
                    if symbol_count > 1:
                        return False
    return True

# Gets next spot (first period in string)
# def get_next_unassigned_var(state):
#     for index in range(len(state)):
#         if state[index] == ".":
#             return index


# Gets next spot (most constrained spot)
def get_next_unassigned_var(unused_vals):
    most_constrained = 0
    most_constrained_val = math.inf
    for index in unused_vals.keys():
        if 1 < len(unused_vals[index]) < most_constrained_val:
            most_constrained = index
            most_constrained_val = len(unused_vals[index])
    return most_constrained, most_constrained_val


# Gets a possible value in the spot using neighbors set
# def get_sorted_values(state, var):
#     values = list()
#     for char in symbol_set:
#         if helper(state, var, char):
#             values.append(char)
#     return values


# Get_sorted_values helper method
# def helper(state, var, char):
#     for neighbor in neighbors[var]:
#         if state[neighbor] == char:
#             return False
#     return True


# Main algorithm to solve sudoku puzzle, part 1
# def csp(state):
#     global count
#     count += 1
#     if "." not in set(state):
#         return state
#     var = get_next_unassigned_var(state)
#     for val in get_sorted_values(state, var):
#         new_state = state[:var] + str(val) + state[var+1:]
#         result = csp(new_state)
#         if result is not None:
#             return result
#     return None


# Goal test
def goal_test(unused_vals):
    for key in unused_vals.keys():
        if len(unused_vals[key]) > 1:
            return False
    return True


# Main algorithm to solve sudoku puzzle; constraint satisfaction
def csp(unused_vals):
    global count
    count += 1
    var, var_value = get_next_unassigned_var(unused_vals)
    if var_value == math.inf:
        return unused_vals
    for val in unused_vals[var]:
        solved = list()
        solved.append(var)
        new_unused_vals = unused_vals.copy()
        new_unused_vals[var] = val
        propagation_result = constraint_propagation(new_unused_vals, solved)
        while propagation_result is not "N" and propagation_result is not False:
            new_unused_vals = propagation_result
            new_unused_vals, solved = propagation_2(new_unused_vals)
            propagation_result = constraint_propagation(new_unused_vals, solved)
        if propagation_result is "N":
            result = csp(new_unused_vals)
            if result is not None:
                return result
    return None


# Creates initial dictionary for constraint propagation
def initial_conditions(state):
    possible_values = dict()
    solved = list()
    for square in range(N**2):
        if state[square] != ".":
            possible_values[square] = state[square]
            solved.append(square)
        else:
            possible_values[square] = symbol_set
    result = constraint_propagation(possible_values, solved)
    while result is not "N":
        possible_values = result
        possible_values, solved = propagation_2(possible_values)
        result = constraint_propagation(possible_values, solved)
    return possible_values


# Constraint propagation (for every solved square, remove possible values from its
# neighbors)
def constraint_propagation(possible_values, solved):
    changed = False
    for square in solved:
        value = possible_values[square]
        for neighbor in neighbors[square]:
            if value in possible_values[neighbor]:
                remove_index = possible_values[neighbor].index(value)
                new_string = \
                    possible_values[neighbor][:remove_index] + \
                    possible_values[neighbor][remove_index + 1:]
                # new_list = list(possible_values[neighbor])
                # new_string = ""
                # for char in new_list:
                #     if char != value:
                #         new_string += char
                changed = True
                if len(new_string) == 0:
                    return False
                if len(new_string) == 1:
                    solved.append(neighbor)
                possible_values[neighbor] = new_string
    if not changed:
        return "N"
    return possible_values


# Sudoku logic piece number two (if value appears in only one set of possible values in the
# constraint set, then set that index equal to that value
def propagation_2(possible_values):
    solved = list()
    for constraint_set in constraint_sets:
        for value in symbol_set:
            val_count = 0
            recent = ""
            for neighbor in constraint_set:
                if value in possible_values[neighbor]:
                    val_count += 1
                    recent = neighbor
                    if val_count > 1:
                        break
            if val_count == 1:
                solved.append(recent)
                possible_values[recent] = value
    return possible_values, solved


# Test Code
def test():
    global count
    global neighbors
    global constraint_sets
    global symbol_set
    puzzle_num = 0
    total_time = 0
    total_calls = 0
    for line in open("sudoku_puzzles_1.txt"):
        # if puzzle_num > 50:  # Stops after puzzle 50
        #     break
        # if puzzle_num == 20:  # File 2 Testing
        #     puzzle_num += 1
        #     continue
        # if puzzle_num == 12 or puzzle_num == 105 or puzzle_num == 140:  # File 3 Testing
        #     puzzle_num += 1
        #     continue
        print("Puzzle Number:", puzzle_num)
        puzzle_num += 1
        line = line.rstrip()
        global_variables(len(line))  # Sets global variables (N, subblock)
        constraint_creation()  # Dictionary of neighbors for each block and constraint sets
        start = perf_counter()
        usable_vals = initial_conditions(line)  # Initial state and initial usable vals
        solution = csp(usable_vals)
        end = perf_counter()
        display_board(solution)  # Displays the board
        if not advanced_check(solution):  # Checks to see whether a sudoku puzzle works
            print("Failure")
            break
        print("Time taken:", end-start)  # Individual statistics
        print("Number of Calls:", count)
        print()
        total_time += end-start  # Total statistics
        total_calls += count
        count = 0
        neighbors = dict()
        constraint_sets = list()
        symbol_set = '123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    print("Total time taken:", total_time)
    print("Total calls:", total_calls)


# Turn in Code
def turn_in():
    global count
    global neighbors
    global constraint_sets
    global symbol_set
    total_time = 0
    total_calls = 0
    file = sys.argv[1]
    for line in open(file):
        line = line.rstrip()
        global_variables(len(line))  # Sets global variables (N, subblock)
        constraint_creation()  # Dictionary of neighbors for each block and constraint sets
        start = perf_counter()
        usable_vals = initial_conditions(line)  # Initial state and initial usable vals
        solution = csp(usable_vals)
        end = perf_counter()
        print("Size:", N)
        turn_in_display_board(solution)
        print("Time taken:", end - start)  # Individual statistics
        print("Number of Calls:", count)
        print()
        total_time += end - start  # Total statistics
        total_calls += count
        count = 0
        neighbors = dict()
        constraint_sets = list()
        symbol_set = '123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    print("Total time taken:", total_time)
    print("Total calls:", total_calls)


test()
# turn_in()
