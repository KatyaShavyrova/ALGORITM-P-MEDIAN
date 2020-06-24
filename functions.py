import random
import copy
import numpy as np


def dijkstra_algorithm(graph, vertex, length):
    """Модифицирует граф, превращая его в матрицу растояний по алгоритму Дейкстра"""
    line = graph[vertex]
    S = set([0])
    for _ in range(length):
        w, item = min(
            enumerate(line),
            key=lambda item: np.inf if item[0] in S else item[1]
        )
        S.add(w)
        for v, k in enumerate(line):
            line[v] = min(k, item+graph[v, w])


def create_distance_matrix(data):
    """Создает матрицу расстояний из данны и заполяет ее расстояниями"""
    start, end, value = max(data, key=lambda item: max(item[0], item[1]))
    length = max(start, end)

    distance_matrix = np.full((length, length), np.inf)
    np.fill_diagonal(distance_matrix, 0)

    for start, end, value in data:
        start -= 1
        end -= 1
        distance_matrix[start, end] = value
        distance_matrix[end, start] = value
    for i in range(length):
        dijkstra_algorithm(distance_matrix, i, length)
    return distance_matrix


def create_vertices(data):
    """Создает множество всех вершин"""
    vertices = set()
    for start, end, _ in data:
        vertices.add(start-1)
        vertices.add(end-1)
    return vertices


def calculate_gear_ratio(distance_matrix, all_vertices, enter_vertices):
    """Считает придаточные числа"""
    return sum(
        map(
            min,
            map(
                lambda index: map(lambda i: distance_matrix[i, index], enter_vertices),
                all_vertices
            )
        )
    )


def teitz_bart_algorithm(distance_matrix, vertices, count_vertices=2):
    """Алгоритм Тейца и Барта"""
    #1
    enter_vertices = random.sample(vertices, count_vertices)
    step_vertices = vertices - set(enter_vertices)
    #2
    external_gear_ratio = calculate_gear_ratio(distance_matrix, vertices, enter_vertices)
    prep_vertex_sets = np.array([enter_vertices for _ in range(count_vertices)])
    for vertex in step_vertices:
        np.fill_diagonal(prep_vertex_sets, vertex)
        internal_gear_ratios = [(calculate_gear_ratio(distance_matrix, vertices, i), i) for i in prep_vertex_sets]
        #3
        min_internal_gear_ratios = min(
            internal_gear_ratios,
            key=lambda item: item[0]
        )
        #3.2
        if external_gear_ratio - min_internal_gear_ratios[0] > 0:
            external_gear_ratio, enter_vertices = copy.deepcopy(min_internal_gear_ratios)
    #4
    if list(enter_vertices) in prep_vertex_sets.tolist():
        return teitz_bart_algorithm(distance_matrix, vertices, count_vertices)
    #5
    return enter_vertices + np.array([1 for _ in range(count_vertices)])
