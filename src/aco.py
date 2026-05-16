import numpy as np
from constraints import (
    is_feasible,
    calculate_route_distance
)

class AntColonyOptimizer:

    def __init__(self,
                 num_customers,
                 vehicle_capacity,
                 distance_matrix,
                 demands,
                 num_ants=20,
                 num_iterations=100,
                 alpha=1,
                 beta=2,
                 evaporation=0.5):

        self.num_customers = num_customers
        self.vehicle_capacity = vehicle_capacity
        self.distance_matrix = distance_matrix
        self.demands = demands

        self.num_ants = num_ants
        self.num_iterations = num_iterations

        self.alpha = alpha
        self.beta = beta
        self.evaporation = evaporation

        self.pheromone = np.ones(
            (num_customers + 1,
             num_customers + 1)
        )

    def build_solution(self):

        unvisited = set(
            range(1, self.num_customers + 1)
        )

        routes = []

        while unvisited:

            route = [0]
            current_node = 0
            current_load = 0

            while True:

                feasible_customers = []

                for customer in unvisited:

                    if is_feasible(
                        current_load,
                        self.demands[customer],
                        self.vehicle_capacity
                    ):
                        feasible_customers.append(customer)

                if not feasible_customers:
                    break

                probabilities = []

                for customer in feasible_customers:

                    tau = (
                        self.pheromone[current_node][customer]
                        ** self.alpha
                    )

                    eta = (
                        1 /
                        self.distance_matrix[current_node][customer]
                    ) ** self.beta

                    probabilities.append(tau * eta)

                probabilities = np.array(probabilities)
                probabilities = (
                    probabilities /
                    probabilities.sum()
                )

                next_customer = np.random.choice(
                    feasible_customers,
                    p=probabilities
                )

                route.append(next_customer)

                current_load += (
                    self.demands[next_customer]
                )

                unvisited.remove(next_customer)

                current_node = next_customer

            route.append(0)

            routes.append(route)

        return routes

    def optimize(self):

        best_routes = None
        best_distance = float("inf")

        distance_history = []

        for iteration in range(self.num_iterations):

            all_routes = []
            all_costs = []

            for ant in range(self.num_ants):

                routes = self.build_solution()

                total_distance = 0

                for route in routes:

                    total_distance += (
                        calculate_route_distance(
                            route,
                            self.distance_matrix
                        )
                    )

                all_routes.append(routes)
                all_costs.append(total_distance)

                if total_distance < best_distance:

                    best_distance = total_distance
                    best_routes = routes

            # Evaporation
            self.pheromone *= (
                1 - self.evaporation
            )

            # Update pheromone
            for routes, cost in zip(
                all_routes,
                all_costs
            ):

                for route in routes:

                    for i in range(len(route) - 1):

                        a = route[i]
                        b = route[i + 1]

                        self.pheromone[a][b] += (
                            1.0 / cost
                        )

            distance_history.append(best_distance)

            print(
                f"Iteration {iteration+1} "
                f"| Best Distance: "
                f"{best_distance:.2f}"
            )

        return (
            best_routes,
            best_distance,
            distance_history
        )