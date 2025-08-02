def greedy_scheduler(nodes, tasks):
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
