import math


# ----------------------------
# Distance function
# ----------------------------
def euclidean(a, b):
    return math.sqrt((a["x"] - b["x"])**2 + (a["y"] - b["y"])**2)


# ----------------------------
# GA assignment validity
# ----------------------------
def check_all_assignments_valid(assignment, num_groups):
    return all(0 <= a < num_groups for a in assignment)


# ----------------------------
# UAV capacity per group
# ----------------------------
def check_group_capacity(group, max_capacity=10):
    return sum(c["demand"] for c in group) <= max_capacity


# ----------------------------
# Full solution feasibility check
# ----------------------------
def check_solution(groups, num_groups, max_capacity=10):
    for k in range(num_groups):
        if k not in groups:
            return False

        group = groups[k]

        # empty group constraint
        if len(group) == 0:
            return False

        # capacity constraint
        if not check_group_capacity(group, max_capacity):
            return False

    return True


# ----------------------------
# Penalty function (GA fitness support)
# ----------------------------
def compute_penalty(groups, max_capacity=10, alpha=10, beta=30, gamma=5):
    """
    groups: {stop_id: [customers]}
    """

    penalty = 0

    for k, customers in groups.items():

        # -------------------------
        # Capacity penalty
        # -------------------------
        total_demand = sum(c["demand"] for c in customers)

        if total_demand > max_capacity:
            penalty += alpha * (total_demand - max_capacity) ** 2

        # -------------------------
        # Empty cluster penalty
        # -------------------------
        if len(customers) == 0:
            penalty += beta

        # -------------------------
        # Imbalance penalty
        # -------------------------
        if len(customers) > 6:
            penalty += gamma * (len(customers) - 6)

        # -------------------------
        # Spatial dispersion penalty (IMPORTANT FIX)
        # encourages compact clusters for ACO efficiency
        # -------------------------
        if len(customers) > 1:
            cx = sum(c["x"] for c in customers) / len(customers)
            cy = sum(c["y"] for c in customers) / len(customers)

            spread = sum(
                math.sqrt((c["x"] - cx)**2 + (c["y"] - cy)**2)
                for c in customers
            )

            penalty += 0.1 * spread

    return penalty