from simulator import Node, Task
from schedulers import ilp_scheduler

def test_ilp_assigns_all_when_capacity_allows():
    nodes = [Node(10, 10, 10)]
    tasks = [Task(2, 2, 2), Task(3, 3, 3)]
    asg = ilp_scheduler(nodes, tasks, alpha=1.0)
    assert len(asg) == 2  # both fit

def test_ilp_prefers_lower_energy_when_throughput_ties():
    n1 = Node(4, 4, 4)
    n2 = Node(4, 4, 4)
    heavy  = Task(4, 4, 4)
    small1 = Task(2, 2, 2)
    small2 = Task(2, 2, 2)
    asg = ilp_scheduler([n1, n2], [heavy, small1, small2], alpha=0.5)
    assigned = set(asg.keys())
    assert small1 in assigned and small2 in assigned
    assert heavy not in assigned
