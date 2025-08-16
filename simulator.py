import random

class Node:
    def __init__(self, cpu, mem, battery):
        self.cpu = cpu          # remaining CPU capacity
        self.mem = mem          # remaining memory capacity
        self.battery = battery  # remaining battery “budget”

    def can_run(self, task) -> bool:
        """
        Return True only if this node still has enough
        CPU, memory, and battery to take on the task.
        """
        return (
            self.cpu     >= task.cpu_req and
            self.mem     >= task.mem_req and
            self.battery >= task.energy_req
        )

    def assign(self, task) -> bool:
        """
        If the node can run the task, deduct the resources
        and return True.  Otherwise do nothing and return False.
        """
        if not self.can_run(task):
            return False

        self.cpu     -= task.cpu_req
        self.mem     -= task.mem_req
        self.battery -= task.energy_req
        return True


class Task:
    def __init__(self, cpu_req, mem_req, energy_req):
        self.cpu_req   = cpu_req
        self.mem_req   = mem_req
        self.energy_req = energy_req


def random_nodes(count, seed=None):
    """
    Return a list of Node objects with random capacities.
    CPU and memory: 8‒16 units   •   Battery: 20‒40 units.
    """
    if seed is not None:
        random.seed(seed)

    return [
        Node(
            cpu=random.randint(8, 16),
            mem=random.randint(8, 16),
            battery=random.randint(20, 40)
        )
        for _ in range(count)
    ]


def random_tasks(count, seed=None):
    """
    Return a list of Task objects with random requirements.
    CPU and memory needs: 1‒6 units   •   Energy: 1‒4 units.
    """
    if seed is not None:
        random.seed(seed + 12345)   # offset so nodes/tasks differ

    return [
        Task(
            cpu_req=random.randint(1, 6),
            mem_req=random.randint(1, 6),
            energy_req=random.randint(1, 4)
        )
        for _ in range(count)
    ]

if __name__ == "__main__":
    from schedulers import greedy_scheduler

    # create a tiny synthetic scenario
    nodes = random_nodes(5)
    tasks = random_tasks(20)

    assignments = greedy_scheduler(nodes, tasks)

    print(f"Greedy scheduler placed {len(assignments)}/{len(tasks)} tasks")

if __name__ == "__main__":
    import copy
    from schedulers import greedy_scheduler, ilp_scheduler
    from metrics import throughput, energy_used, jain_fairness, log_to_csv

    # Build identical starting state for both schedulers
    nodes_g = random_nodes(5, seed=2)
    tasks   = random_tasks(30, seed=2)
    before  = copy.deepcopy(nodes_g)

    # --- Greedy ---
    asg_g = greedy_scheduler(nodes_g, tasks)
    tp_g  = throughput(asg_g, len(tasks))
    en_g  = energy_used(before, nodes_g)
    per_node_energy_g = [b.battery - a.battery for b, a in zip(before, nodes_g)]
    fair_g = jain_fairness(per_node_energy_g)
    print(f"[Greedy] Placed: {len(asg_g)}/{len(tasks)}  Throughput: {tp_g:.0%}  Energy: {en_g}  Fairness: {fair_g:.2f}")
    log_to_csv("results.csv", dict(nodes=len(nodes_g), tasks=len(tasks),
                                   scheduler="greedy", throughput=tp_g,
                                   energy_used=en_g, fairness=fair_g))

    # --- ILP (fresh copy of pre-schedule state) ---
    nodes_i = copy.deepcopy(before)
    asg_i = ilp_scheduler(nodes_i, tasks, alpha=0.8)
    tp_i  = throughput(asg_i, len(tasks))
    en_i  = energy_used(before, nodes_i)
    per_node_energy_i = [b.battery - a.battery for b, a in zip(before, nodes_i)]
    fair_i = jain_fairness(per_node_energy_i)
    print(f"[ILP   ] Placed: {len(asg_i)}/{len(tasks)}  Throughput: {tp_i:.0%}  Energy: {en_i}  Fairness: {fair_i:.2f}")
    log_to_csv("results.csv", dict(nodes=len(nodes_i), tasks=len(tasks),
                                   scheduler="ilp", throughput=tp_i,
                                   energy_used=en_i, fairness=fair_i))
