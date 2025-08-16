from simulator import Node, Task

def test_can_run_true():
    n = Node(10, 10, 10); t = Task(4, 3, 2)
    assert n.can_run(t)

def test_can_run_false():
    n = Node(2, 2, 2); t = Task(5, 1, 1)
    assert not n.can_run(t)

def test_assign_success():
    n = Node(10, 10, 10); t = Task(3, 3, 3)
    assert n.assign(t) and (n.cpu, n.mem, n.battery) == (7, 7, 7)

def test_assign_failure():
    n = Node(1, 1, 1); t = Task(2, 2, 2)
    assert not n.assign(t) and (n.cpu, n.mem, n.battery) == (1, 1, 1)
