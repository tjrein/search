from copy import deepcopy
import sys

def is_complete(state):
    for row in state:
        print row
        if -1 in row:
            print "failing out"
            return False

    print "puzzle complete"
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
    display_state(dimensions, clone)
    is_complete(clone)

def main():
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        load_file(filename)
    else:
        print "Please specify a file to load"

if __name__ == '__main__':
    main()
