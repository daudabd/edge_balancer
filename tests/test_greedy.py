from simulator import Node, Task
from simulator import random_nodes, random_tasks


def test_can_run_true():
    node = Node(cpu=10, mem=10, battery=10)
    task = Task(cpu_req=4, mem_req=3, energy_req=2)
    assert node.can_run(task) is True


def test_can_run_false():
    node = Node(cpu=2, mem=2, battery=2)
    task = Task(cpu_req=5, mem_req=1, energy_req=1)
    assert node.can_run(task) is False


def test_assign_success():
    node = Node(cpu=10, mem=10, battery=10)
    task = Task(cpu_req=3, mem_req=3, energy_req=3)
    success = node.assign(task)
    assert success is True
    assert (node.cpu, node.mem, node.battery) == (7, 7, 7)


def test_assign_failure():
    node = Node(cpu=1, mem=1, battery=1)
    task = Task(cpu_req=2, mem_req=2, energy_req=2)
    success = node.assign(task)
    assert success is False
    # resources stay unchanged
    assert (node.cpu, node.mem, node.battery) == (1, 1, 1)

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
