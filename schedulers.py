from typing import Dict

# ---------- Greedy baseline ----------
def greedy_scheduler(nodes, tasks) -> Dict[object, object]:
    """Assign each task to the first node with enough resources."""
    assignments = {}
    for task in tasks:
        for node in nodes:
            if (node.cpu     >= task.cpu_req and
                node.mem     >= task.mem_req and
                node.battery >= task.energy_req):
                assignments[task] = node
                node.cpu     -= task.cpu_req
                node.mem     -= task.mem_req
                node.battery -= task.energy_req
                break
    return assignments


# ---------- ILP optimizer (PuLP) ----------
try:
    import pulp as pl
except Exception:
    pl = None  # we'll raise a helpful error inside ilp_scheduler


def ilp_scheduler(nodes, tasks, alpha: float = 0.8) -> Dict[object, object]:
    """
    0/1 ILP: assign tasks to nodes.
    alpha∈[0,1]: higher -> prioritize throughput, lower -> prioritize energy saving.
    Returns {task_obj: node_obj} and deducts node capacities like greedy.
    """
    if pl is None:
        raise RuntimeError("PuLP not installed. Activate venv and `pip install pulp`.")

    N = range(len(nodes))
    T = range(len(tasks))

    # Decision: x[i,j] = 1 if task i runs on node j
    x = pl.LpVariable.dicts(
        "x", [(i, j) for i in T for j in N],
        lowBound=0, upBound=1, cat="Binary"
    )

    prob = pl.LpProblem("EdgeScheduler", pl.LpMaximize)

    # Each task on at most one node
    for i in T:
        prob += pl.lpSum(x[(i, j)] for j in N) <= 1, f"task_{i}_one_node"

    # Node capacity constraints
    for j in N:
        prob += pl.lpSum(tasks[i].cpu_req    * x[(i, j)] for i in T) <= nodes[j].cpu,     f"cpu_cap_{j}"
        prob += pl.lpSum(tasks[i].mem_req    * x[(i, j)] for i in T) <= nodes[j].mem,     f"mem_cap_{j}"
        prob += pl.lpSum(tasks[i].energy_req * x[(i, j)] for i in T) <= nodes[j].battery, f"bat_cap_{j}"

    # Objective: maximize throughput, minimize energy (weighted by alpha)
    throughput_expr = pl.lpSum(x[(i, j)] for i in T for j in N)
    energy_expr     = pl.lpSum(tasks[i].energy_req * x[(i, j)] for i in T for j in N)

    # Light normalization so alpha behaves intuitively
    max_throughput = max(1, len(tasks))
    max_energy     = max(1, sum(t.energy_req for t in tasks))
    prob += alpha * (throughput_expr / max_throughput) - (1 - alpha) * (energy_expr / max_energy)

    # Solve silently
    solver = pl.PULP_CBC_CMD(msg=False)
    status = prob.solve(solver)
    if pl.LpStatus[status] not in ("Optimal", "Feasible"):
        return {}

    # Build assignment and deduct resources
    assignments = {}
    for i in T:
        for j in N:
            val = pl.value(x[(i, j)])
            if val and val > 0.5:
                assignments[tasks[i]] = nodes[j]
                nodes[j].cpu     -= tasks[i].cpu_req
                nodes[j].mem     -= tasks[i].mem_req
                nodes[j].battery -= tasks[i].energy_req
                break
    return assignments
