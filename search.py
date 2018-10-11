from copy import deepcopy
import random
import sys

def pprint(state):
    for row in state:
        print row

def is_valid_move(piece_inds, pattern, state):
    for inds in piece_inds:
        row, col = inds
        new_row, new_col = [row+pattern[0], col+pattern[1]]
        potential_move = state[new_row][new_col]

        if potential_move != 0 and potential_move != state[row][col]:
            return False

    return True

def apply_move_clone(state, move, pieces):
    new_state = clone_state(state)
    apply_move(new_state, move, pieces)
    return new_state

def apply_move(state, move, pieces):
    piece, direction = move
    pattern = get_move_pattern(direction)
    indices = pieces.get(piece)

    update_piece_inds = []

    for ind in indices:
        row, col = ind
        new_row, new_col = [row+pattern[0], col+pattern[1]]

        state[new_row][new_col] = piece
        state[row][col] = 0
        update_piece_inds.append((new_row, new_col))

    pieces[piece] = update_piece_inds 

def check_move_for_piece(state, piece, pieces):
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

        if is_valid_move(piece_inds, pattern, state):
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

def validate_moves(state, pieces):
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
    clone.insert(0, dimensions)
    for row in clone:
        print ','.join(str(val) for val in row) + ','

def clone_state(state):
    return deepcopy(state)

def load_file(filename):
    read_data = None

    state = []
    with open(filename, 'r') as f:
        for line in f:
            stripped_line = line.replace(',', ' ').strip().split()
            sanitized_line = [int(val) for val in stripped_line]
            state.append(sanitized_line)

    random_walks(state, 3)
    
def is_same_state(state, other):
    for i, row in enumerate(state):
        for j, col in enumerate(row):
            if state[i][j] != other[i][j]:
                return False
    return True

def normalize_state(state):
    next_ind = 3

    for i, row in enumerate(state):
        for j, col in enumerate(row):
            if state[i][j] == next_ind:
                next_ind += 1
            elif state[i][j] > next_ind:
                swap_index(next_ind, state[i][j], state)
                next_ind += 1

def swap_index(ind_1, ind_2, state):
    for i, row in enumerate(state):
        for j, col in enumerate(row):
            if state[i][j] == ind_1:
                state[i][j] = ind_2
            elif state[i][j] == ind_2:
                state[i][j] = ind_1

def random_walks(state, executions):
    clone = clone_state(state)
    dimensions = state.pop(0)
    
    display_state(clone.pop(0), clone)
    for i in range(3):
        if is_complete(state):
            return "Solved"

        pieces = get_all_pieces(state)

        valid_moves = validate_moves(state, pieces)
        rand_int = random.randint(0, len(valid_moves) - 1)

        move = valid_moves[rand_int]

        apply_move(state, move, pieces)
        print "\n" + str(move)
        print
        display_state(dimensions, clone_state(state))
        #print "\n" +str(move)
        


def main():
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        load_file(filename)
    else:
        print "Please specify a file to load"

if __name__ == '__main__':
    main()
