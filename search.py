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
        print "pattern", pattern
        print "inds", inds
        print "new location", new_location

        cell_val = state[new_location[0]][new_location[1]]
        print '\n'
        print "cell_val", cell_val
        print "state item", state[row][col]

        if cell_val != 0 and cell_val != state[row][col]:
            print "HOW YA DOING THEN"
            return False

    return True
         

def check_possible_moves(piece, piece_inds, state):
    directions = ('u', 'd', 'l', 'r')
    possible_moves = []
    row, col = piece_inds

    move_patterns = {
        'u': [-1, 0],
        'd': [1, 0],
        'l': [0, -1],
        'r': [0, 1]
    }

    for direction in directions:
        pattern = move_patterns[direction]

        if add_pattern_to_move(piece_inds, pattern, state):
            possible_moves.append((piece, direction))

    print possible_moves

def validate_move(state):
    chosen_piece = 2
    valid_moves = []

    piece_inds = []

    pprint(state)

    for i, row in enumerate(state):
        for j, piece in enumerate(row):
            if piece == chosen_piece:
                piece_inds.append((i, j))


    check_possible_moves(chosen_piece, piece_inds, state)


    return valid_moves

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
    #display_state(dimensions, clone)

    validate_move(clone)

def main():
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        load_file(filename)
    else:
        print "Please specify a file to load"

if __name__ == '__main__':
    main()
