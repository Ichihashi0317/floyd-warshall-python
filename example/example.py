from sys import stdin


####  Paste floyd_warshall.py source code here  ####
class FloydWarshall: ...


def main():
    readline = stdin.readline

    N, M, Q = map(int, readline().split())

    edges = []
    for _ in range(M):
        A, B, C = map(int, readline().split())
        edges.append((A - 1, B - 1, C))

    queries = []
    edge_enabled = [True] * M
    for _ in range(Q):
        com, *args = map(int, readline().split())
        if com == 1:
            edge_idx = args[0] - 1
            queries.append((com, edge_idx))
            edge_enabled[edge_idx] = False
        else:
            x, y = args
            queries.append((com, (x - 1, y - 1)))

    fw = FloydWarshall(N, inf=N * 10**9)
    for edge_idx, (A, B, C) in enumerate(edges):
        if edge_enabled[edge_idx]:
            fw.add_edge(A, B, C)
            fw.add_edge(B, A, C)
    fw.solve()  # dist matrix is now valid; update_dists=True becomes available

    answers = []
    for com, query in reversed(queries):
        if com == 1:
            A, B, C = edges[query]
            fw.add_edge(A, B, C, update_dists=True)
            fw.add_edge(B, A, C, update_dists=True)
        else:
            x, y = query
            d = fw.dist[x][y]
            answers.append(-1 if d == fw.inf else d)

    print("\n".join(map(str, reversed(answers))))


if __name__ == "__main__":
    main()
