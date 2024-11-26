
import heapq


def Prims(G):

    visited = [False] * len(G)
    min_heap = []
    heapq.heappush(min_heap, (0, 0, None))
    mst = []

    while min_heap:
        weight, curr_vertex, parent = heapq.heappop(min_heap)
        if visited[curr_vertex]:
            continue

        visited[curr_vertex] = True
        if parent is not None:
            mst.append((parent, curr_vertex, weight))

        for next in range(len(G)):
            if G[curr_vertex][next] != 0 and not visited[next]:
                heapq.heappush(min_heap, (G[curr_vertex][next], next, curr_vertex))

    return mst
