from queue import PriorityQueue

def a_star(graph, start, goal, heuristics):
    open_list = PriorityQueue()
    open_list.put((0, start))
    came_from = {}
    g_score = {node: float('inf') for node in graph}
    g_score[start] = 0

    while not open_list.empty():
        _, current = open_list.get()

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path, g_score[goal]

        for neighbor, cost in graph[current].items():
            tentative_g = g_score[current] + cost
            if tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score = tentative_g + heuristics[neighbor]
                open_list.put((f_score, neighbor))

    return None, float('inf')

# Example weighted graph
graph = {
    'A': {'B': 1, 'C': 3},
    'B': {'D': 1, 'E': 5},
    'C': {'F': 2},
    'D': {'E': 1, 'G': 3},
    'E': {'G': 2},
    'F': {'G': 2},
    'G': {}
}

# Example heuristic values (estimated cost to reach goal 'G')
heuristics = {
    'A': 7,
    'B': 6,
    'C': 5,
    'D': 3,
    'E': 2,
    'F': 1,
    'G': 0
}

# Run A* from A to G
path, cost = a_star(graph, 'A', 'G', heuristics)
print("Shortest Path:", path)
print("Total Cost:", cost)
