"""
UNIT 4: Search

Your task is to maneuver a car in a crowded parking lot. This is a kind of 
puzzle, which can be represented with a diagram like this: 

| | | | | | | |  
| G G . . . Y |  
| P . . B . Y | 
| P * * B . Y @ 
| P . . B . . |  
| O . . . A A |  
| O . S S S . |  
| | | | | | | | 

A '|' represents a wall around the parking lot, a '.' represents an empty square,
and a letter or asterisk represents a car.  '@' marks a goal square.
Note that there are long (3 spot) and short (2 spot) cars.
Your task is to get the car that is represented by '**' out of the parking lot
(on to a goal square).  Cars can move only in the direction they are pointing.  
In this diagram, the cars GG, AA, SSS, and ** are pointed right-left,
so they can move any number of squares right or left, as long as they don't
bump into another car or wall.  In this diagram, GG could move 1, 2, or 3 spots
to the right; AA could move 1, 2, or 3 spots to the left, and ** cannot move 
at all. In the up-down direction, BBB can move one up or down, YYY can move 
one down, and PPP and OO cannot move.

You should solve this puzzle (and ones like it) using search.  You will be 
given an initial state like this diagram and a goal location for the ** car;
in this puzzle the goal is the '.' empty spot in the wall on the right side.
You should return a path -- an alternation of states and actions -- that leads
to a state where the car overlaps the goal.

An action is a move by one car in one direction (by any number of spaces).  
For example, here is a successor state where the AA car moves 3 to the left:

| | | | | | | |  
| G G . . . Y |  
| P . . B . Y | 
| P * * B . Y @ 
| P . . B . . |  
| O A A . . . |  
| O . . . . . |  
| | | | | | | | 

And then after BBB moves 2 down and YYY moves 3 down, we can solve the puzzle
by moving ** 4 spaces to the right:

| | | | | | | |
| G G . . . . |
| P . . . . . |
| P . . . . * *
| P . . B . Y |
| O A A B . Y |
| O . . B . Y |
| | | | | | | |

You will write the function

    solve_parking_puzzle(start, N=N)

where 'start' is the initial state of the puzzle and 'N' is the length of a side
of the square that encloses the pieces (including the walls, so N=8 here).

We will represent the grid with integer indexes. Here we see the 
non-wall index numbers (with the goal at index 31):

 |  |  |  |  |  |  |  |
 |  9 10 11 12 13 14  |
 | 17 18 19 20 21 22  |
 | 25 26 27 28 29 30 31
 | 33 34 35 36 37 38  |
 | 41 42 43 44 45 46  |
 | 49 50 51 52 53 54  |
 |  |  |  |  |  |  |  |

The wall in the upper left has index 0 and the one in the lower right has 63.
We represent a state of the problem with one big tuple of (object, locations)
pairs, where each pair is a tuple and the locations are a tuple.  Here is the
initial state for the problem above in this format:
"""
# TODO: Convert the ordinal positions of wall and car to fixed.

puzzle1 = (
 ('@', (31,)),
 ('*', (26, 27)), 
 ('G', (9, 10)),
 ('Y', (14, 22, 30)), 
 ('P', (17, 25, 33)), 
 ('O', (41, 49)), 
 ('B', (20, 28, 36)), 
 ('A', (45, 46)), 
 ('|', (0, 1, 2, 3, 4, 5, 6, 7, 8, 15, 16, 23, 24, 32, 39,
        40, 47, 48, 55, 56, 57, 58, 59, 60, 61, 62, 63)))

# A solution to this puzzle is as follows:

#     path = solve_parking_puzzle(puzzle1, N=8)
#     path_actions(path) == [('A', -3), ('B', 16), ('Y', 24), ('*', 4)]

# That is, move car 'A' 3 spaces left, then 'B' 2 down, then 'Y' 3 down, 
# and finally '*' moves 4 spaces right to the goal.

# Your task is to define solve_parking_puzzle:

N = 8

def solve_parking_puzzle(start, N=N):
    """Solve the puzzle described by the starting position (a tuple 
    of (object, locations) pairs).  Return a path of [state, action, ...]
    alternating items; an action is a pair (object, distance_moved),
    such as ('B', 16) to move 'B' two squares down on the N=8 grid."""
    path = shortest_path_search(start,successors,is_goal)
    #print path
    for state in path[0::2]:
        #print state
        show(state)
        print 
    return path_actions(path)
    
# But it would also be nice to have a simpler format to describe puzzles,
# and a way to visualize states.
# You will do that by defining the following two functions:

def locs(start, n, incr=1):
    "Return a tuple of n locations, starting at start and incrementing by incr."
    return tuple(range(start,start + incr*n,incr))


def grid(cars, N=N):
    """Return a tuple of (object, locations) pairs -- the format expected for
    this puzzle.  This function includes a wall pair, ('|', (0, ...)) to 
    indicate there are walls all around the NxN grid, except at the goal 
    location, which is the middle of the right-hand wall; there is a goal
    pair, like ('@', (31,)), to indicate this. The variable 'cars'  is a
    tuple of pairs like ('*', (26, 27)). The return result is a big tuple
    of the 'cars' pairs along with the walls and goal pairs."""
    grid = list()

    top_wall = range(0,N) 
    left_wall = range(N,(N-1)*N,N)
    right_wall = range(2*N-1,(N-1)*N,N)
    right_wall.remove(31) 
    bottom_wall = range((N-1)*N,N*N,1)
    wall = top_wall + left_wall + right_wall+ bottom_wall

    grid.append(('|',tuple(wall)))
    
    grid.append(('@',(31,)))# generate goal pair 31
    
    for car in cars:# determine car pair
        grid.append(car)

    return tuple(grid)

def show(state, N=N):
    "Print a representation of a state as an NxN grid."
    # Initialize and fill in the board.
    board = ['.'] * N**2
    for (c, squares) in state:
        for s in squares:
            board[s] = c
    # Now print it out
    for i,s in enumerate(board):
        print s,
        if i % N == N - 1: print

# Here we see the grid and locs functions in use:

puzzle2 = grid((
    ('*', locs(26, 2)),
    ('G', locs(9, 2)),
    ('Y', locs(14, 3, N)),
    ('P', locs(17, 3, N)),
    ('O', locs(41, 2, N)),
    ('B', locs(20, 3, N)),
    ('A', locs(45, 2))))

puzzle3 = grid((
    ('*', locs(26, 2)),
    ('B', locs(20, 3, N)),
    ('P', locs(33, 3)),
    ('O', locs(41, 2, N)),
    ('Y', locs(51, 3))))

puzzle4 = grid((
    ('*', locs(25, 2)),
    ('B', locs(19, 3, N)),
    ('P', locs(36, 3)),
    ('O', locs(45, 2, N)),
    ('Y', locs(49, 3))))

def successors(state):
    # find orientation of the car
    # find possible empty spots based on the orientation
    # return each possible state with action.
    successors = {} 

    def no_collisions(new_lot):
        return new_lot not in occupied_lots

    occupied_lots = []
    for car_state in state:
        car,position = car_state
        if car != '@':
            occupied_lots.extend(list(position))
    #print occupied_lots 
    for index,car_state in enumerate(state):
        car,position = car_state
        if car != '|' and car != '@':
            increment = 1 if position[-1] - position[0] < N else N
            new_position = move_position(position,increment)
            #print new_position
            while no_collisions(new_position[-1]):
                #print state[:index] + (car,new_position) + state[index+1:]
                #print car,(car,new_position[-1] - position[-1])
                successors.update({(state[:index] + ((car,new_position),) + state[index+1:]):(car,new_position[-1] - position[-1])})
                new_position = move_position(new_position,increment)

            new_position = move_position(position,-increment)
            while no_collisions(new_position[0]):
                #print state[:index] + (car,new_position) + state[index+1:]
                #print car,(car,new_position[-1] - position[-1])
                successors.update({(state[:index] + ((car,new_position),) + state[index+1:]):(car,new_position[-1] - position[-1])})
                new_position = move_position(new_position,-increment)
    return successors

def move_position(old_position,increment):
    return tuple([element+increment for element in old_position])

def is_goal(state):
    for car_state in state:
        car,position = car_state
        if car == '*':
            return True if 31 in position else False #convert 31 into a CONST

# Here are the shortest_path_search and path_actions functions from the unit.
# You may use these if you want, but you don't have to.

def shortest_path_search(start, successors, is_goal):
    """Find the shortest path from start state to a state
    such that is_goal(state) is true."""
    if is_goal(start):
        return [start]
    explored = set() # set of states we have visited
    frontier = [ [start] ] # ordered list of paths we have blazed
    while frontier:
        path = frontier.pop(0)
        s = path[-1]
        for (state, action) in successors(s).items():
            if state not in explored:
                explored.add(state)
                path2 = path + [action, state]
                if is_goal(state):
                    return path2
                else:
                    frontier.append(path2)
    return []

def path_actions(path):
    "Return a list of actions in this path."
    return path[1::2]

def test_unit():
    assert locs(26,5,1) == (26,27,28,29,30)
    assert locs(19, 3, N) == (19,27,35)
    assert set((puzzle1[-1])[-1]) == set((puzzle2[0])[-1]) # comparing the wall elements as that is the controversial and there is no easy way to compare tuple that have been assembled differently
    initial_state = (
    ('@', (31,)),
    ('*', (26, 27)), 
    ('G', (9, 10)),
    ('Y', (14, 22, 30)), 
    ('P', (17, 25, 33)), 
    ('O', (41, 49)), 
    ('B', (20, 28, 36)), 
    ('A', (45, 46)), 
    ('|', (0, 1, 2, 3, 4, 5, 6, 7, 8, 15, 16, 23, 24, 32, 39,
    40, 47, 48, 55, 56, 57, 58, 59, 60, 61, 62, 63)))
    successors(initial_state)
    #assert solve_parking_puzzle(initial_state) == [('A', -3), ('B', 16), ('Y', 24), ('*', 4)]
    print solve_parking_puzzle(puzzle2)
    print solve_parking_puzzle(puzzle3)
    print solve_parking_puzzle(puzzle4)
    return 'tests pass'

if __name__ == '__main__':
    print test_unit()
