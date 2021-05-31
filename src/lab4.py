import pandas as pd
from random import randint


class Node:
    def __init__(self, idx, weight):
        self.idx = idx
        self.weight = weight
        self.t_level = 0

    def __str__(self):
        fmt = t_level_color + "'{0}'" + reset_color + ": {1}" + reset_color
        return fmt.format(self.idx, self.t_level)


def split_by_levels(nodes):
    levels = [[nodes[0]]]
    free_nodes = nodes[1:]
    current_level = 1

    while len(free_nodes) > 0:
        levels.append([])
        for free_node in free_nodes:
            to_current_level = False

            for prev_node in levels[current_level - 1]:
                edge_weight = matrix[prev_node.idx][free_node.idx]
                if edge_weight > 0:
                    to_current_level = True
                    free_node.t_level = max(free_node.t_level, prev_node.t_level + prev_node.weight + edge_weight)

            for node in levels[current_level]:
                if matrix[free_node.idx][node.idx] > 0 or matrix[node.idx][free_node.idx] > 0:
                    to_current_level = False
                    break

            if to_current_level:
                levels[current_level].append(free_node)

        free_nodes = free_nodes[len(levels[current_level]):]
        current_level += 1
    return levels


def find_critical_way(connection_matrix, weight):
    child, parent, distance = N * [N * []], N * [N * []], N * [0]
    critical_way = [levels[-1][-1].idx]

    for i in range(N):
        for j in range(N):
            if connection_matrix[i][j] != 0:
                child[i] = child[i] + [j]
                parent[j] = parent[j] + [i]

    distance[0] = weight[0]
    for i in range(N):
        for j in range(len(child[i])):
            if distance[i] + weight[child[i][j]] > distance[child[i][j]]:
                distance[child[i][j]] = distance[i] + weight[child[i][j]]

    while critical_way[0] != 0:
        temp_max = 0
        for i in range(len(parent[critical_way[0]])):
            if distance[parent[critical_way[0]][i]] >= distance[temp_max]:
                temp_max = parent[critical_way[0]][i]
        critical_way.insert(0, temp_max)

    return critical_way, child, distance


def transite(levels):
    res = []
    mins = list(map(lambda level: min([node.t_level for node in level]), levels))
    for i in range(len(levels) - 1):
        for current_node in levels[i]:
            if current_node.t_level >= mins[i + 1]:
                res.append(current_node)
    return res


def clasterisation(critical_way, child, distance, weights):
    clasterized_edges = N * [[]]

    for i in range(1, len(critical_way) - 1):
        edge_claster = []
        left, right = critical_way[i-1], critical_way[i+1]

        for j in range(len(child[left])):
            if right in child[child[left][j]] and child[left][j] != critical_way[i]:
                edge_claster.append(child[left][j])

        for j in range(len(edge_claster)):
            for k in range(j, len(edge_claster)):
                if distance[edge_claster[k]] > distance[edge_claster[j]]:
                    temp = edge_claster[k]
                    edge_claster[k] = edge_claster[j]
                    edge_claster[j] = temp

        temp_edge = 0
        while temp_edge < len(edge_claster):
            temp_weight = weights[edge_claster[temp_edge]]
            level_edges = []

            j = temp_edge + 1
            while j < len(edge_claster):
                if temp_weight + weights[edge_claster[j]] <= weights[critical_way[i]]:
                    temp_weight += weights[edge_claster[j]]
                    if not level_edges:
                        level_edges = [edge_claster[temp_edge], edge_claster[j]]
                    else:
                        level_edges = level_edges + [edge_claster[j]]
                    del edge_claster[j]
                    j -= 1
                j += 1

            if level_edges:
                del edge_claster[temp_edge]
                clasterized_edges[i] = clasterized_edges[i] + [tuple(level_edges)]
            else:
                temp_edge += 1

    return clasterized_edges


matrix = [[0, randint(1, 4), randint(1, 4), randint(1, 4), randint(1, 4), 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, randint(1, 4), 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, randint(1, 4), 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, randint(1, 4), 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, randint(1, 4), 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, randint(1, 4), randint(1, 4), 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, randint(1, 4), randint(1, 4), 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, randint(1, 4), 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, randint(1, 4), randint(1, 4), randint(1, 4), 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, randint(1, 4), randint(1, 4), 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, randint(1, 4), 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, randint(1, 4), 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, randint(1, 4), 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, randint(1, 4), randint(1, 4), randint(1, 4), randint(1, 4), randint(1, 4), randint(1, 4), 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, randint(1, 4), 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, randint(1, 4), 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, randint(1, 4), 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, randint(1, 4), 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, randint(1, 4), 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, randint(1, 4), 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, randint(1, 4), randint(1, 4), randint(1, 4), randint(1, 4), 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, randint(1, 4), 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, randint(1, 4), 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, randint(1, 4), 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, randint(1, 4), 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, randint(1, 4), randint(1, 4), randint(1, 4), 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, randint(1, 4)],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, randint(1, 4)],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, randint(1, 4)],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

weights = [1, 2, 4, 1, 1, 2, 1, 3, 8, 6, 4, 5, 2, 1, 7, 5, 7, 4, 2, 3, 1, 2, 6, 1, 1, 1, 3, 4, 5, 1, 2]

N = len(matrix)

bold_color = "\033[1m"
reset_color = "\x1B[0m"
t_level_color = "\x1B[35m"
critical_color = "\x1B[34m"
separator = "\x1B[37m" + '=' * (4 * N + 3) + reset_color

pd.set_option('display.expand_frame_repr', False)
print(separator + bold_color + '\nConnectivity matrix:\n' + reset_color,
      pd.DataFrame(matrix, columns=[x for x in range(31)]))

print(separator, bold_color + '\nVertex weight:\n' + reset_color +
      ''.join(["{:4}".format(w) for w in weights]))

print(separator, bold_color + '\nBreakdown by levels ' + reset_color + '(vertex number: t_level):')

nodes = [Node(i, weights[i]) for i in range(N)]

levels = split_by_levels(nodes)
for level in levels:
    print('\t' + ' | '.join(map(lambda node: '{:^22}'.format(str(node)), level)))
print(separator)

print(bold_color + 'Critical path:' + reset_color)
critical, child_arr, distance = find_critical_way(matrix, weights)
print(' -> '.join(map(lambda node: '{:^2}'.format(critical_color + str(node) + reset_color), critical)))
print('\tTcr =', distance[-1])
print(separator)

print(bold_color + 'Clustered vertices:' + reset_color)
claster_edges = clasterisation(critical, child_arr, distance, weights)
for level in range(len(claster_edges)):
    if claster_edges[level]:
        print('\tLevel ' + str(level) + ': ' + str(claster_edges[level]))
print(separator)

# print(bold_color + 'Вершини з ознакою неявної транзитності ' + reset_color + '(номер вершини : t_level):')
# result = transite(levels)
# print(' -> '.join(map(lambda node: '{:^7}'.format(str(node)), result)))
