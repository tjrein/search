from copy import deepcopy
import sys

def pprint(state):
    for row in state:
        print row

def add_pattern_to_move(piece_inds, pattern, state):

    for inds in piece_inds:
        row, col = inds
        new_location = [row + pattern[0], col + pattern[1]]

        cell_val = state[new_location[0]][new_location[1]]
        if cell_val != 0 and cell_val != state[row][col]:
            return False

    return True

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

        if add_pattern_to_move(piece_inds, pattern, state):
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

    initial_state = []
    with open(filename, 'r') as f:
        for line in f:
            stripped_line = line.replace(',', ' ').strip().split()
            sanitized_line = [int(val) for val in stripped_line]
            initial_state.append(sanitized_line)

    dimensions = initial_state.pop(0)
    clone = clone_state(initial_state)
    pieces = get_all_pieces(clone)
    
    valid_moves = validate_moves(clone, pieces)

    moves_for_piece = check_move_for_piece(clone, 4, pieces)
    test_moves = check_move_for_piece(clone, 2, pieces)

    apply_move(clone, test_moves[0], pieces)
    
    test_moves2 = check_move_for_piece(clone, 4, pieces)
    apply_move(clone, test_moves2[0], pieces)

def main():
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        load_file(filename)
    else:
        print "Please specify a file to load"

if __name__ == '__main__':
    main()
