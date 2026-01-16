import pytest
from floyd_warshall import FloydWarshall


def test_dist_available_in_initial_state():
    fw = FloydWarshall(3)
    d = fw.dist
    assert d[0][0] == 0
    assert d[0][1] == fw.inf


def test_dirty_state_and_recovery():
    fw = FloydWarshall(4)
    fw.add_edge(0, 1, 3)
    fw.solve()

    fw.add_edge(1, 2, 4, update_dists=False)  # makes it dirty
    with pytest.raises(RuntimeError):
        _ = fw.dist
    with pytest.raises(RuntimeError):
        fw.add_edge(0, 2, 1, update_dists=True)
    with pytest.raises(RuntimeError):
        fw.has_negative_cycle()

    fw.solve()  # recovers
    _ = fw.dist
    fw.add_edge(0, 2, 1, update_dists=True)
    assert fw.has_negative_cycle() is False

    assert fw.dist[0][2] == 1


def test_negative_cycle_detection():
    fw = FloydWarshall(3)
    fw.add_edge(0, 1, 1)
    fw.add_edge(1, 2, 1)
    fw.solve()
    assert fw.has_negative_cycle() is False

    fw.add_edge(2, 0, -3)  # negative cycle
    fw.solve()
    assert fw.has_negative_cycle() is True
