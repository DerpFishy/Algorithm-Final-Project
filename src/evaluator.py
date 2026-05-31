# evaluator.py

from aco_optimizer import dist
from constraint import compute_penalty

def evaluate_solution(chrom, customers, stops, aco):
    stop_order, assignment = chrom

    stop_map = {s["id"]: s for s in stops}
    groups = {i: [] for i in range(len(stops))}

    for c, g in zip(customers, assignment):
        groups[g].append(c)

    total_cost = 0

    # truck cost
    for i in range(len(stop_order) - 1):
        a = stop_map[stop_order[i]]
        b = stop_map[stop_order[i + 1]]
        total_cost += dist(a, b)

    # UAV cost (ACO)
    for g, custs in groups.items():
        depot = stop_map[g]
        _, cost = aco.solve(depot, custs)
        total_cost += cost

    # constraints (centralized)
    penalty = compute_penalty(groups)

    return total_cost + penalty