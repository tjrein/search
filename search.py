from copy import deepcopy
from collections import deque
import random
import sys
import time

def is_valid_move(piece_inds, pattern, state, piece):
    for inds in piece_inds:
        row, col = inds
        new_row, new_col = [row+pattern[0], col+pattern[1]]
        potential_move = state[new_row][new_col]
        win_condition = piece is 2 and potential_move is -1

        if potential_move != 0 and potential_move != state[row][col] and not win_condition:
            return False

    return True

def apply_move_clone(state, move):
    new_state = clone_state(state)
    apply_move(new_state, move)
    return new_state

def apply_move(state, move):
    pieces = get_all_pieces(state)
    piece, direction = move
    pattern = get_move_pattern(direction)
    indices = pieces.get(piece)

    update_piece_inds = []

    for ind in indices:
        row, col = ind
        new_row, new_col = [row+pattern[0], col+pattern[1]]
        state[row][col] = 0
        update_piece_inds.append((new_row, new_col))

    for ind in update_piece_inds:
        row, col = ind
        state[row][col] = piece

def check_move_for_piece(state, piece):
    pieces = get_all_pieces(state)
    indices = pieces.get(piece)
    valid_moves = check_possible_moves(piece, indices, state)
    return valid_moves

def get_move_pattern(direction):
    move_patterns = {
        'u': [-1, 0],
        'd': [1, 0],
        'l': [0, -1],
        'r': [0, 1]
    }[direction]

    return move_patterns

def check_possible_moves(piece, piece_inds, state):
    directions = ('u', 'd', 'l', 'r')
    moves = []

    for direction in directions:
        pattern = get_move_pattern(direction)

        if is_valid_move(piece_inds, pattern, state, piece):
            moves.append((piece, direction))

    return moves

def get_all_pieces(state):
    pieces = {}

    for i, row in enumerate(state):
        for j, piece in enumerate(row):
            if piece > 1:
                if piece in pieces:
                    pieces[piece].append((i, j))
                else:
                    pieces[piece] = [(i, j)]

    return pieces

def validate_moves(state):
    pieces = get_all_pieces(state)
    possible_moves = []

    for piece, indices in pieces.items():
        possible_moves += check_possible_moves(piece, indices, state)

    return possible_moves

def is_complete(state):
    for row in state:
        if -1 in row:
            return False
    return True

def display_state(dimensions, clone):
    print ','.join(str(val) for val in dimensions) + ','
    for row in clone:
        print ','.join(str(val) for val in row) + ','

def clone_state(state):
    return deepcopy(state)

def general_search(state, method):
    dimensions = state.pop(0)
    nodes = {}
    
    start = time.time()
    goal_node = search(clone_state(state), method, nodes)
    end = time.time()

    elapsed_time = "{:.2f}".format((end - start))
    output_path(nodes, goal_node["id"], dimensions, elapsed_time)

def iterative_deepening(state):
    dimensions = state.pop(0)
    limit = 1

    goal_node = None

    start = time.time()
    while True:
        nodes = {}
        goal_node = search(clone_state(state), "DFS", nodes, limit=limit)
        if goal_node is not None:
            end = time.time()
            break
        else:
            limit += 1

    elapsed_time = "{:.2f}".format((end - start))
    output_path(nodes, goal_node["id"], dimensions, elapsed_time)

def search(state, method, nodes, limit=None):
    frontier = deque()
    explored = []
    node_id = 0
    parent_id = 0

    current_node = {
        'state': clone_state(state),
        'action': None,
        'parent': None,
        'id': 0,
        'depth': 0
    }

    nodes[0] = current_node
    frontier.append(current_node)

    while frontier:
        #use queue if BFS, stack if DFS
        if method == "BFS":
            current_node = frontier.popleft()
        if method == "DFS":
            current_node = frontier.pop()

        parent_id = current_node["id"]
        depth = current_node["depth"]
        current_state = current_node["state"]
        normalized_state = clone_state(current_state)

        if is_complete(normalized_state):
            return current_node

        explored.append(current_node)

        #For IDS, don't expand if the depth of the node is at the limit
        if depth is limit:
            continue

        #expand children
        possible_moves = validate_moves(clone_state(current_state))
        for move in possible_moves:
            possible_state = apply_move_clone(current_state, move)
            possible_state_normalized = normalize_state(clone_state(possible_state))

            if not repeat_state(explored, possible_state_normalized) and not repeat_state(frontier, possible_state_normalized):
                #if not in explored and fringe, add nodes to fringe
                node_id += 1
                nodes[node_id] = {
                    "state": possible_state,
                    "parent": parent_id,
                    "action": move,
                    "id": node_id,
                    "depth": depth + 1
                }
                frontier.append(nodes[node_id])

        #cuttoff for iterative deepening
        #If node depth has reached limit, no additional elements will be on fringe
        if not frontier:
            return None

def output_path(nodes, node_id, dimensions, elapsed_time):
    actions = []
    finished_state = nodes[node_id]["state"]

    print
    while nodes[node_id]["parent"] is not None:
        actions.append(nodes[node_id]["action"])
        node_id = nodes[node_id]["parent"]

    actions.reverse()

    for action in actions:
        print action

    display_state(dimensions, finished_state)
    print len(nodes), elapsed_time, len(actions)

def repeat_state(nodes, found_state):
    normal_found_state = normalize_state(found_state)
    for node in nodes:
        if is_same_state(normalize_state(node["state"]), normal_found_state):
            return True
    return False

def is_same_state(state, other):
    for i, row in enumerate(state):
        for j, col in enumerate(row):
            if state[i][j] != other[i][j]:
                return False
    return True

def normalize_state(state):
    next_ind = 3

    clone = clone_state(state)

    for i, row in enumerate(clone):
        for j, col in enumerate(row):
            if clone[i][j] == next_ind:
                next_ind += 1
            elif clone[i][j] > next_ind:
                swap_index(next_ind, clone[i][j], clone)
                next_ind += 1

    return clone

def swap_index(ind_1, ind_2, state):
    for i, row in enumerate(state):
        for j, col in enumerate(row):
            if state[i][j] == ind_1:
                state[i][j] = ind_2
            elif state[i][j] == ind_2:
                state[i][j] = ind_1

def random_walks(state, executions):
    dimensions = state.pop(0)

    #initial starting state
    display_state(dimensions, state)

    for i in range(executions):
        #get moves
        possible_moves = validate_moves(state)

        #select random move from list
        rand_int = random.randint(0, len(possible_moves) - 1)
        move = possible_moves[rand_int]
        
        #execute move
        apply_move(state, move)

        #normalize game state
        normal_state = normalize_state(state)

        #display move and resulting state
        print "\n" + str(move) + "\n"
        display_state(dimensions, state)
       
        #exit if puzzle is complete, otherwise continue next execution
        if is_complete(normal_state):
            return

def load_file(filename):
    state = []
    with open(filename, 'r') as f:
        for line in f:
            stripped_line = line.replace(',', ' ').strip().split()
            sanitized_line = [int(val) for val in stripped_line]
            state.append(sanitized_line)

    return state

def main():
    #load files
    level_0 = load_file('SBP-level0.txt')
    level_1 = load_file('SBP-level1.txt')
    
    #random walks
    random_walks(clone_state(level_0), 3)

    #breadth first search
    general_search(clone_state(level_1), "BFS")

    #depth first search
    general_search(clone_state(level_1), "DFS")

    #iterative deepening
    iterative_deepening(clone_state(level_1))

if __name__ == '__main__':
    main()
