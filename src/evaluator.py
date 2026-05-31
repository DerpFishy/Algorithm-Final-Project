from aco_optimizer import dist
from constraint import compute_penalty


def evaluate_solution(chrom, customers, stops, aco):
    stop_order, assignment = chrom

    stop_map = {s["id"]: s for s in stops}

    groups = {i: [] for i in range(len(stops))}

    for c, g in zip(customers, assignment):
        groups[g].append(c)

    total_cost = 0

    # ----------------------------
    # TRUCK COST
    # ----------------------------
    for i in range(len(stop_order) - 1):
        a = stop_map[stop_order[i]]
        b = stop_map[stop_order[i + 1]]
        total_cost += dist(a, b)

    # ----------------------------
    # IMPORTANT FIX: reset ACO memory
    # ----------------------------
    aco.reset()

    # ----------------------------
    # UAV COST (ACO per cluster)
    # ----------------------------
    for g, custs in groups.items():
        hub = stop_map[g]
        _, cost = aco.solve(hub, custs)
        total_cost += cost

    # ----------------------------
    # PENALTY (scaled to prevent domination)
    # ----------------------------
    penalty = compute_penalty(groups)

    return total_cost + 0.1 * penalty