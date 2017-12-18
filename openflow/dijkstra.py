"""
Name:          Sean Hassett

An implementation of Dijkstra's Algorithm for finding the shortest path
between points in a graph
"""


def get_shortest_path(graph, source):
    vertices = graph[0]
    edges = graph[1]

    dist = dict()
    prev = dict()

    for v in vertices:
        dist[v] = float("inf")
        prev[v] = None

    dist[source] = 0

    Q = list(vertices)
    while len(Q) > 0:
        u = Q[0]
        d = dist[u]
        for v in Q:
            if dist[v] < d:
                u = v
                d = dist[v]
        Q.remove(u)

        for v in edges[u]:
            alt = dist[u] + edges[u][v]
            if alt < dist[v]:
                dist[v] = alt
                prev[v] = u
    return prev
