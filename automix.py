#!/usr/bin/env python3

"""
Module comment here.

The idea is to find the diameter in a metric MST.
"""

from dataclasses import dataclass

def distance_matrix(points, metric):
    return {p1: {p2: metric(p1, p2) for p2 in points}
            for p1 in points}


def minimum_spanning_tree(graph):
    """Prim's algorithm.

    TODO use a priority queue.
    """

    tree = set()

    first_node = list(graph.keys())[0]
    tree.add(first_node)

    edges = []

    def best_edge():
        min_dist = None
        argmin_dist = None
        for p1 in tree:
            for p2, dist in graph[p1].items():
                if p2 not in tree and dist is not None:
                    if min_dist is None or dist < min_dist:
                        min_dist = dist
                        argmin_dist = (p1, p2)
        return (argmin_dist, min_dist)

    next_edge, dist = best_edge()
    while next_edge is not None:
        old, new = next_edge
        edges.append((next_edge, dist))
        tree.add(new)
        next_edge, dist = best_edge()

    return edges


def shortest_distance_matrix(tree):
    """Floyd-Warshall algorithm.
    """

    nodes = set(a for edge, dist in tree for a in edge)
    distance = {v: {w: None for w in nodes} for v in nodes}
    link = {v: {w: None for w in nodes} for v in nodes}

    for v in nodes:
        distance[v][v] = 0

    for edge, dist in tree:
        v, w = edge
        distance[v][w] = distance[w][v] = dist
        link[v][w] = w
        link[w][v] = v

    for intermediate in nodes:
        for start in nodes:
            for end in nodes:
                first_distance = distance[start][intermediate]
                second_distance = distance[intermediate][end]

                current_distance = distance[start][end]

                if first_distance is None or second_distance is None:
                    continue

                if current_distance is None or current_distance >= first_distance + second_distance:
                    distance[start][end] = distance[end][start] = first_distance + second_distance

                    if link[start][intermediate] is not None:
                        link[start][end] = link[start][intermediate]
    return (distance, link)


def find_path(link, source, dest):
    current = source
    path = [current]
    while current != dest:
        if current is None:
            return None
        current = link[current][dest]
        path.append(current)

    return path


def read_files(summary):
    tracks = []
    with open(summary) as f:
        lines = f.read().splitlines()
        for line in lines:
            words = line.split()
            camelot, bpm, filename = words[0], float(words[1]), ' '.join(words[2:])
            camelot_wedge = int(camelot[:-1])
            camelot_ring = camelot[-1]
            track = Track(filename, camelot_wedge, camelot_ring, bpm)
            tracks.append(track)
    return tracks


def camelot_distance(track1, track2):
    wedge1, ring1 = track1.camelot_wedge, track1.camelot_ring
    wedge2, ring2 = track2.camelot_wedge, track2.camelot_ring

    if ring1 == ring2:
        return min((wedge1 - wedge2) % 12, (wedge2 - wedge1) % 12)
    if wedge1 == wedge2:
        return 1
    return None


def track_distance(track1, track2):
    camelot = camelot_distance(track1, track2)
    if camelot is None:
        return None
    else:
        return camelot * camelot + ((track1.bpm - track2.bpm) / 6) ** 2

@dataclass(frozen=True)
class Track:
    filename: str
    camelot_wedge: int
    camelot_ring: str
    bpm: float

tracks = read_files('dw4.csv')

graph = distance_matrix(tracks, track_distance)
mst = minimum_spanning_tree(graph)
ones_mst = [(e, 1) for e, dist in mst]
shortest_distance, link = shortest_distance_matrix(ones_mst)

furthest = ()
furthest_dist = None
for t1 in tracks:
    for t2 in tracks:
        dist = shortest_distance[t1][t2]
        if not furthest_dist or shortest_distance[t1][t2] > furthest_dist:
            furthest_dist = shortest_distance[t1][t2]
            furthest = (t1, t2)

t1, t2 = furthest
for track in find_path(link, t1, t2):
    print(track)
