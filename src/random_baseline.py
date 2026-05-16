import random

from constraints import (
    is_feasible,
    calculate_route_distance
)

class RandomRouting:

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

        customers = list(
            range(1, self.num_customers + 1)
        )

        random.shuffle(customers)

        routes = []

        current_route = [0]
        current_load = 0

        for customer in customers:

            demand = self.demands[customer]

            # Check capacity
            if is_feasible(
                current_load,
                demand,
                self.vehicle_capacity
            ):

                current_route.append(customer)
                current_load += demand

            else:
                # Finish current route
                current_route.append(0)

                routes.append(current_route)

                # Start new route
                current_route = [0, customer]

                current_load = demand

        # Finish last route
        current_route.append(0)

        routes.append(current_route)

        return routes

    def evaluate(self, routes):

        total_distance = 0

        for route in routes:

            total_distance += (
                calculate_route_distance(
                    route,
                    self.distance_matrix
                )
            )

        return total_distance

    def run(self):

        routes = self.generate_solution()

        total_distance = self.evaluate(routes)

        return routes, total_distance