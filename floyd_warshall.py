class FloydWarshall:
    """Floyd-Warshall all-pairs shortest paths (APSP) for a weighted directed graph.

    This class is designed for competitive programming.

    Typical workflow:
        1. Call `add_edge()` to add directed edges (relaxations).
        2. Call `solve()` to compute all-pairs shortest-path distances.

    Advanced usage:
        Incremental update (optional):
            If you have already called `solve()` (or the graph is still empty), you may call
            `add_edge(update_dists=True)` to propagate a single relaxation in O(n^2) time.

            This is useful when you have already computed APSP once and then insert a new
            edge or decrease an edge weight. If the new edge does not improve the direct
            cost, the call is a no-op.

            Supported updates:
                Only relaxations are supported (edge insertion / weight decrease that can
                shorten shortest paths). Weight increases and edge deletions are not
                supported.

        Negative cycles:
            Call `has_negative_cycle()` after `solve()`.
            If it returns True, shortest-path distances are not well-defined in general;
            do not interpret `dist` as shortest distances.

    Matrix state:
        The internal matrix `_dist` is either:
            - up-to-date: reflects APSP for the current graph, or
            - stale: one or more relaxations were added without propagation.

        When the matrix is stale, the following operations are forbidden and raise
        `RuntimeError`:
            - accessing `dist`
            - calling `has_negative_cycle()`
            - calling `add_edge(update_dists=True)`

        Call `solve()` to make the matrix up-to-date again.

    Complexity:
        - Memory: O(n^2)
        - `__init__()`: O(n^2) time
        - `add_edge(update_dists=False)`: O(1) time
        - `add_edge(update_dists=True)`: O(n^2) time
        - `solve()`: O(n^3) time
        - `dist` (property): O(1) access
        - `has_negative_cycle()`: O(n) time

    Args:
        num_v: Number of vertices, labeled 0..num_v-1.
        inf: Sentinel for unreachable distances. Defaults to float('inf').
            If you provide a finite value, it must be strictly larger than any reachable
            shortest-path distance.
    """

    def __init__(self, num_v: int, inf: int | float = float("inf")) -> None:
        """Create an instance with an empty graph.

        Initializes `_dist` with 0 on the diagonal and `inf` elsewhere.
        The matrix starts up-to-date because it already represents APSP for the empty graph.

        Args:
            num_v: Number of vertices.
            inf: Sentinel for unreachable distances.

        Raises:
            AssertionError: If `inf` is not positive.
        """
        assert inf > 0

        self._n = num_v
        self.inf = inf
        self._dist = [
            [0 if i == j else inf for j in range(num_v)] for i in range(num_v)
        ]
        self._needs_solve = False

    def add_edge(
        self,
        u: int,
        v: int,
        weight: int | float = 1,
        update_dists: bool = False,
    ) -> None:
        """Relax the directed edge `u` -> `v` with the given `weight`.

        Updates the direct cost only if `weight` is smaller than the current value.

        If `update_dists=True`, this method also propagates this relaxation to all pairs in
        O(n^2) time. This requires that the distance matrix is up-to-date.

        Args:
            u: Source vertex.
            v: Destination vertex.
            weight: Edge weight.
            update_dists: If True, propagate this relaxation to all pairs.

        Raises:
            RuntimeError: If `update_dists=True` and the matrix is stale.
            AssertionError: If `u`/`v` are out of range, or if `weight >= inf`.
        """
        assert 0 <= u < self._n
        assert 0 <= v < self._n
        assert weight < self.inf

        if update_dists and self._needs_solve:
            raise RuntimeError(
                "Distance matrix is stale; call solve() before add_edge(update_dists=True)"
            )

        if weight >= self._dist[u][v]:
            return

        # Relax the direct edge cost
        self._dist[u][v] = weight

        if not update_dists:
            self._needs_solve = True
            return

        # Propagate the relaxation to all pairs
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
        """Compute APSP distances using the Floyd-Warshall algorithm.

        After this call, the distance matrix becomes up-to-date.

        If the matrix is already up-to-date, this method returns immediately.

        Returns:
            The distance matrix (no copy). Make a copy before modifying.
        """
        assert self.inf > 0

        if not self._needs_solve:
            return self._dist

        n = self._n
        inf = self.inf
        dist = self._dist

        for k in range(n):
            for i in range(n):
                if dist[i][k] == inf:
                    continue
                dik = dist[i][k]
                for j in range(n):
                    if dist[k][j] == inf:
                        continue
                    if (d := dik + dist[k][j]) < dist[i][j]:
                        dist[i][j] = d

        self._needs_solve = False
        return self._dist

    @property
    def dist(self) -> list[list[int | float]]:
        """All-pairs shortest-path distance matrix.

        This requires that the distance matrix is up-to-date.

        Returns:
            The distance matrix (no copy). Make a copy before modifying.

        Raises:
            RuntimeError: If the matrix is stale.
        """
        if self._needs_solve:
            raise RuntimeError(
                "Distance matrix is stale; call solve() before accessing dist"
            )
        return self._dist

    def has_negative_cycle(self) -> bool:
        """Check whether the graph contains a negative cycle.

        This requires that the distance matrix is up-to-date.

        Returns:
            True if there exists a vertex `v` such that `dist[v][v] < 0`.

        Raises:
            RuntimeError: If the matrix is stale.
        """
        if self._needs_solve:
            raise RuntimeError(
                "Distance matrix is stale; call solve() before has_negative_cycle()"
            )
        return any(self._dist[v][v] < 0 for v in range(self._n))
