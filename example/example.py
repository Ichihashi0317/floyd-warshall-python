class FloydWarshall:
    """
    Floyd-Warshall all-pairs shortest paths (APSP) for a weighted directed graph.

    This implementation is designed for competitive programming.

    Overview:
        - Use `add_edge()` to set directed edges (relaxation).
        - Call `solve()` to compute all-pairs shortest-path distances.

    Optional incremental update:
        After the distance matrix is valid (i.e., after `solve()` or in the initial
        empty-graph state), you may call `add_edge(..., update_dists=True)` to
        update the all-pairs distances in O(n^2) time for an edge relaxation.

        Notes:
            Only relaxations are supported (edge insertion / weight decrease that can
            shorten shortest paths). Weight increases and edge deletions are not supported.

    Negative cycles:
        Call `has_negative_cycle()` after `solve()` (or in the initial empty-graph state).
        If it returns True, shortest-path distances are not well-defined in general; do not
        interpret `dist` as shortest distances.

    Complexity:
        - Memory: O(n^2)
        - solve(): O(n^3) time
        - add_edge(update_dists=True): O(n^2) time
        - add_edge(update_dists=False): O(1) time

    Args:
        num_v: Number of vertices (0..num_v-1).
        inf: Sentinel for unreachable distances. Defaults to float('inf').
             If you provide a finite value, it must be sufficiently large to exceed any
             reachable shortest-path distance.
    """

    def __init__(self, num_v: int, inf: int | float = float("inf")) -> None:
        assert inf > 0

        self._n = num_v
        self.inf = inf
        self._dist = [
            [0 if i == j else inf for j in range(num_v)] for i in range(num_v)
        ]
        self._needs_solve = False

    @property
    def dist(self) -> list[list[int | float]]:
        """
        All-pairs shortest-path distance matrix.

        Returns:
            The distance matrix when it is valid (after `solve()` or in the initial empty-graph state).

        Raises:
            RuntimeError: If the matrix is not currently valid (i.e., `_needs_solve` is True).
        """
        if self._needs_solve:
            raise RuntimeError("Call solve() before accessing dist")
        return self._dist

    def add_edge(
        self,
        u: int,
        v: int,
        weight: int | float = 1,
        update_dists: bool = False,
    ) -> None:
        """
        Add a directed edge u -> v with the given weight (relaxation).

        The internal matrix is updated only if `weight` is smaller than the current value.

        If `update_dists=True`, this method also updates all-pairs distances in O(n^2) time.
        This requires that the all-pairs distance matrix is currently valid.

        Args:
            u: Source vertex.
            v: Destination vertex.
            weight: Edge weight.
            update_dists: If True, propagate the relaxation to all-pairs distances.

        Raises:
            RuntimeError: If `update_dists=True` is used while the matrix is not valid.
        """
        assert 0 <= u < self._n
        assert 0 <= v < self._n
        assert weight < self.inf

        if update_dists and self._needs_solve:
            raise RuntimeError(
                "Call solve() before calling add_edge(update_dists=True)"
            )

        if weight >= self._dist[u][v]:
            return

        # Add an edge (relaxation)
        self._dist[u][v] = weight

        if not update_dists:
            self._needs_solve = True
            return

        # Update all-pairs distances
        n = self._n
        inf = self.inf
        dist = self._dist

        for i in range(n):
            if dist[i][u] == inf:
                continue
            tmp = dist[i][u] + weight
            for j in range(n):
                if dist[v][j] == inf:
                    continue
                d = tmp + dist[v][j]
                if d < dist[i][j]:
                    dist[i][j] = d

    def solve(self) -> list[list[int | float]]:
        """
        Compute all-pairs shortest-path distances by the Floyd–Warshall algorithm.

        After this call, the distance matrix becomes valid (`_needs_solve` becomes False).

        Returns:
            The distance matrix.
        """
        assert self.inf > 0

        n = self._n
        inf = self.inf
        dist = self._dist

        for k in range(n):
            for i in range(n):
                if dist[i][k] == inf:
                    continue
                for j in range(n):
                    if dist[k][j] == inf:
                        continue
                    if (d := dist[i][k] + dist[k][j]) < dist[i][j]:
                        dist[i][j] = d

        self._needs_solve = False
        return self._dist

    def has_negative_cycle(self) -> bool:
        """
        Check whether the graph contains a negative cycle.

        This method requires that the all-pairs distance matrix is currently valid
        (after `solve()` or in the initial empty-graph state).

        Returns:
            True if there exists a vertex v such that dist[v][v] < 0.

        Raises:
            RuntimeError: If called while the matrix is not valid.
        """
        if self._needs_solve:
            raise RuntimeError("Call solve() before calling has_negative_cycle()")
        return any(self._dist[v][v] < 0 for v in range(self._n))


def main():
    N, M, Q = map(int, input().split())

    Edges = []
    for _ in range(M):
        A, B, C = map(int, input().split())
        Edges += [(A - 1, B - 1, C)]

    Queries = []
    is_passable = [True] * M
    for _ in range(Q):
        com, *q = map(int, input().split())
        if com == 1:
            i = q[0] - 1
            Queries += [(com, i)]
            is_passable[i] = False
        else:
            x, y = q
            Queries += [(com, (x - 1, y - 1))]

    fw = FloydWarshall(N, inf=N * 10**9)
    for i in range(M):
        if not is_passable[i]:
            continue
        A, B, C = Edges[i]
        fw.add_edge(A, B, C)
        fw.add_edge(B, A, C)

    fw.solve()

    answers = []
    for com, q in Queries[::-1]:
        if com == 1:
            A, B, C = Edges[q]
            fw.add_edge(A, B, C, update_dists=True)
            fw.add_edge(B, A, C, update_dists=True)
        else:
            x, y = q
            d = fw.dist[x][y]
            if d == fw.inf:
                d = -1
            answers += [d]

    for d in answers[::-1]:
        print(d)


if __name__ == "__main__":
    main()
