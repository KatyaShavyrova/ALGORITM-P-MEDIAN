from collections import Counter
from src.settings import *
from src.utils import read_data, parse_config
from src.functions import create_distance_matrix, create_vertices, teitz_bart_algorithm

if __name__ == '__main__':
    config = parse_config(CONFIG_FILE)
    count = int(config['DEFAULT']['count'])
    p = int(config['DEFAULT']['p'])
    data = read_data(DATA_FILE)
    vertices = create_vertices(data)
    distance_matrix = create_distance_matrix(data)
    medians = [tuple(teitz_bart_algorithm(distance_matrix, vertices, p)) for i in range(count)]
    counter = Counter(medians).items()
    for key, val in sorted(counter, key=lambda item: item[1], reverse=True):
        print(f"median {key}, amount {val}")
    