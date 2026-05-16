from constraints import (
    is_feasible,
    calculate_route_distance
)

class GreedyNearestNeighbor:

    def __init__(self,
                 num_customers,
                 vehicle_capacity,
                 distance_matrix,
                 demands):

        self.num_customers = num_customers
        self.vehicle_capacity = vehicle_capacity
        self.distance_matrix = distance_matrix
        self.demands = demands

    def generate_solution(self):

        unvisited = set(
            range(1, self.num_customers + 1)
        )

        routes = []

        while unvisited:

            current_route = [0]  # start at depot
            current_node = 0
            current_load = 0

            while True:

                feasible_customers = []

                # check capacity feasibility
                for customer in unvisited:

                    if is_feasible(
                        current_load,
                        self.demands[customer],
                        self.vehicle_capacity
                    ):
                        feasible_customers.append(customer)

                if not feasible_customers:
                    break

                # GREEDY STEP: pick nearest neighbor
                next_customer = min(
                    feasible_customers,
                    key=lambda c: self.distance_matrix[current_node][c]
                )

                current_route.append(next_customer)

                current_load += self.demands[next_customer]

                unvisited.remove(next_customer)

                current_node = next_customer

            current_route.append(0)  # return to depot
            routes.append(current_route)

        return routes

    def evaluate(self, routes):

        total_distance = 0

        for route in routes:

            total_distance += calculate_route_distance(
                route,
                self.distance_matrix
            )

        return total_distance

    def run(self):

        routes = self.generate_solution()
        total_distance = self.evaluate(routes)

        return routes, total_distance