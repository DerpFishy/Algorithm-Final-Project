def is_feasible(current_load,
                customer_demand,
                vehicle_capacity):

    return (
        current_load + customer_demand
        <= vehicle_capacity
    )


def calculate_route_distance(route,
                             distance_matrix):

    total_distance = 0

    for i in range(len(route) - 1):

        a = route[i]
        b = route[i + 1]

        total_distance += distance_matrix[a][b]

    return total_distance