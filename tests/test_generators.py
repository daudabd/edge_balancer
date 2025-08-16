from simulator import random_nodes, random_tasks

def test_random_nodes_range():
    nodes = random_nodes(10, seed=1)
    for n in nodes:
        assert 8 <= n.cpu <= 16
        assert 8 <= n.mem <= 16
        assert 20 <= n.battery <= 40

def test_random_tasks_range():
    tasks = random_tasks(10, seed=1)
    for t in tasks:
        assert 1 <= t.cpu_req <= 6
        assert 1 <= t.mem_req <= 6
        assert 1 <= t.energy_req <= 4
