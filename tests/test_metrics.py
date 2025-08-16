from simulator import Node
from metrics import throughput, energy_used, jain_fairness

def test_throughput():
    assert throughput({1: 1}, 4) == 0.25

def test_energy_used():
    before = [Node(0, 0, 10), Node(0, 0, 10)]
    after  = [Node(0, 0, 7),  Node(0, 0, 10)]
    assert energy_used(before, after) == 3

def test_jain_fairness():
    assert jain_fairness([1, 1]) == 1.0       # perfectly even
    assert jain_fairness([2, 0])  < 1.0       # uneven load
