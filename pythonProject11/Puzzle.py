from collections import deque


def solve_puzzle(Board, Source, Destination):

    def is_valid(cell):
        m, n = cell
        return 0 <= m < len(Board) and 0 <= n < len(Board[0]) and Board[m][n] == '-'

    queue = deque([Source])
    visited = [[False] * len(Board[0]) for _ in range(len(Board))]
    prev_cell = {}
    visited[Source[0]][Source[1]] = True

    while queue:
        current_cell = queue.popleft()
        if current_cell == Destination:
            break

        m, n = current_cell

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dr, dc in directions:
            neighbor = (m + dr, n + dc)

            if is_valid(neighbor) and not visited[neighbor[0]][neighbor[1]]:
                queue.append(neighbor)
                visited[neighbor[0]][neighbor[1]] = True
                prev_cell[neighbor] = current_cell

    if Destination not in prev_cell:
        return None
    path = [Destination]
    while path[-1] != Source:
        path.append(prev_cell[path[-1]])
    path.reverse()

    return path
