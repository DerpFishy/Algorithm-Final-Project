import math
from constraint import compute_penalty


def dist(a, b):
    return math.hypot(a["x"] - b["x"], a["y"] - b["y"])


def evaluate_solution(chrom, customers, stops):
    stop_order, assignment = chrom

    stop_map = {s["id"]: s for s in stops}

    groups = {i: [] for i in range(len(stops))}
    for c, g in zip(customers, assignment):
        if g < 0 or g >= len(stops):
            g = g % len(stops)
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
    # UAV COST (hub-based star model)
    # ----------------------------
    for g, custs in groups.items():
        if not custs:
            continue

        hub = stop_map[g]

        # round-trip UAV cost approximation
        for c in custs:
            d = dist(hub, c)
            total_cost += 2 * (d ** 0.9)  # sublinear UAV cost to encourage grouping

    # ----------------------------
    # PENALTY (normalized)
    # ----------------------------
    penalty = compute_penalty(groups)

    penalty_weight = total_cost / max(1, len(customers))

    return total_cost + 0.05 * penalty * penalty_weight