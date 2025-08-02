from simulator import Node, Task
from schedulers import greedy_scheduler

def test_single_assignment():
    n = Node(10, 10, 10)
    t = Task(5, 5, 5)
    result = greedy_scheduler([n], [t])
    assert t in result and result[t] is n
