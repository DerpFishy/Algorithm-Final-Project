# constraint.py

def check_uav_capacity(customers, max_capacity=10):
    total_demand = sum(c["demand"] for c in customers)
    return total_demand <= max_capacity


def check_empty_group(customers):
    return len(customers) > 0


def check_all_assignments_valid(assignment, num_groups):
    return all(0 <= a < num_groups for a in assignment)


def compute_penalty(groups, max_capacity=10):
    penalty = 0

    for g, customers in groups.items():
        total_demand = sum(c["demand"] for c in customers)

        # overload penalty (stronger)
        if total_demand > max_capacity:
            penalty += (total_demand - max_capacity) ** 2 * 10

        # empty cluster penalty
        if len(customers) == 0:
            penalty += 30

        # imbalance penalty (NEW)
        if len(customers) > 6:
            penalty += (len(customers) - 6) * 5

    return penalty