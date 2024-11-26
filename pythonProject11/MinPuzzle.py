
import heapq


def minEffort(puzzle):
    if len(puzzle) == 0:
        return 0

    start_vertex = "r" + str(0) + "-" + "c" + str(0)
    end_vertex = "r" + str(len(puzzle)-1) + "-" + "c" + str(len(puzzle[0])-1)
    converted_graph = {}

    for m in range(len(puzzle)):
        for n in range(len(puzzle[0])):
            current_cell = "r" + str(m) + "-" + "c" + str(n)
            converted_graph[current_cell] = {}

            if m != 0:
                neighbor_cell = "r" + str(m-1) + "-" + "c" + str(n)
                converted_graph[current_cell][neighbor_cell] = abs(puzzle[m][n] - puzzle[m-1][n])

            if n != 0:
                neighbor_cell = "r" + str(m) + "-" + "c" + str(n-1)
                converted_graph[current_cell][neighbor_cell] = abs(puzzle[m][n] - puzzle[m][n-1])

            if m != (len(puzzle)-1):
                neighbor_cell = "r" + str(m+1) + "-" + "c" + str(n)
                converted_graph[current_cell][neighbor_cell] = abs(puzzle[m][n] - puzzle[m+1][n])

            if n != (len(puzzle[0])-1):
                neighbor_cell = "r" + str(m) + "-" + "c" + str(n+1)
                converted_graph[current_cell][neighbor_cell] = abs(puzzle[m][n] - puzzle[m][n+1])

    return calculate_min_effort(converted_graph, start_vertex, end_vertex)


def calculate_min_effort(graph, start_vertex, end_vertex):
    efforts = {vertex: float('infinity') for vertex in graph}
    efforts[start_vertex] = 0

    pqueue = [(0, start_vertex)]
    while len(pqueue) > 0:
        current_effort, current_vertex = heapq.heappop(pqueue)

        if current_effort > efforts[current_vertex]:
            continue

        for neighbor, weight in graph[current_vertex].items():
            effort = weight

            if effort < efforts[neighbor]:
                efforts[neighbor] = effort
                heapq.heappush(pqueue, (effort, neighbor))

    return efforts[end_vertex]
