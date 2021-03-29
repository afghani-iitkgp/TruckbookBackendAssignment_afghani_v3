from collections import defaultdict
import heapq


def dijkstra_heapq(edges, f, t):
    g = defaultdict(list)

    for l, r, c in edges:
        g[l].append((c, r))

    q = [(0, f, ())]
    seen = set()
    mins = {f: 0}

    while q:
        (cost, v1, path) = heapq.heappop(q)

        if v1 not in seen:
            seen.add(v1)
            path = (v1, path)

            if v1 == t:
                return (cost, path)

            for c, v2 in g.get(v1, ()):
                if v2 in seen:
                    continue
                prev = mins.get(v2, None)
                next = cost + c

                if prev is None or next < prev:
                    mins[v2] = next
                    heapq.heappush(q, (next, v2, path))

    return float("inf"), None


if __name__ == "__main__":
    edges = [
        ("A", "B", 7),
        ("A", "D", 5),
        ("B", "C", 8),
        ("B", "D", 9),
        ("B", "E", 7),
        ("C", "E", 5),
        ("D", "E", 15),
        ("D", "F", 6),
        ("E", "F", 8),
        ("E", "G", 9),
        ("F", "G", 11)
    ]

    print ("=== Dijkstra ===")
    print (edges)
    print ("A -> E:")
    print (dijkstra_heapq(edges, "A", "E"))
    print ("F -> G:")
    print (dijkstra_heapq(edges, "F", "G"))
    print ("A -> G:")
    print (dijkstra_heapq(edges, "A", "G"))
