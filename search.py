from copy import deepcopy
import sys

def pprint(state):
    for row in state:
        print row

def add_pattern_to_move(piece_inds, pattern, state):

    pprint(state)

    for inds in piece_inds:
        row, col = inds
        new_location = [row + pattern[0], col + pattern[1]]

        cell_val = state[new_location[0]][new_location[1]]
        if cell_val != 0 and cell_val != state[row][col]:
            return False

    return True

#def check_move_for_piece(piece, state):
         

def check_possible_moves(piece, piece_inds, state):
    directions = ('u', 'd', 'l', 'r')
    moves = []

    move_patterns = {
        'u': [-1, 0],
        'd': [1, 0],
        'l': [0, -1],
        'r': [0, 1]
    }

    for direction in directions:
        pattern = move_patterns[direction]

        if add_pattern_to_move(piece_inds, pattern, state):
            moves.append((piece, direction))

    return moves


def select_all_pieces(state):
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
    pieces = select_all_pieces(state)
    piece_dict = pieces
    pprint(state)

    print "PIECE_DICT", piece_dict
    possible_moves = []

    for piece, indices in pieces.items():
        possible_moves += check_possible_moves(piece, indices, state)
        print "POSSIBLE_MOVES", possible_moves

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

    validate_moves(clone)

def main():
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        load_file(filename)
    else:
        print "Please specify a file to load"

if __name__ == '__main__':
    main()
