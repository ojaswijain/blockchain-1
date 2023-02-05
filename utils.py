import numpy as np

def write_to_file(filename, data):
    with open(filename, 'w') as f:
        f.write(data)

def read_from_file(filename):
    with open(filename, 'r') as f:
        return f.read()

def get_random_number():
    return np.random.randint(0, 100)

