import csv, os, math

def throughput(assignments, total_tasks):
    """
    Ratio of tasks successfully placed.
    e.g. 0.85 means 85 % of tasks found a home.
    """
    return len(assignments) / total_tasks if total_tasks else 0.0


def energy_used(before_nodes, after_nodes):
    """
    How many battery ‘units’ the whole cluster spent.
    We compare battery totals before and after scheduling.
    """
    start  = sum(n.battery for n in before_nodes)
    finish = sum(n.battery for n in after_nodes)
    return start - finish


def jain_fairness(usages):
    """
    Jain’s fairness index (0‒1). 1.0 == perfectly even load.
    Formula: (Σu)² / (N · Σu²)
    """
    if not usages:
        return 1.0
    num = sum(usages) ** 2
    den = len(usages) * sum(u ** 2 for u in usages)
    return num / den if den else 1.0


def log_to_csv(path, row):
    """
    Append one experiment’s metrics to a CSV file.
    Creates the file & header the first time.
    """
    write_header = not os.path.exists(path)
    with open(path, "a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=row.keys())
        if write_header:
            w.writeheader()
        w.writerow(row)
