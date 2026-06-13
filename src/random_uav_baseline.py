import random

class RandomUAVBaseline:
    def __init__(self, customers, distance_matrix, Qmax, UAV_V):
        self.customers = customers
        self.dist = distance_matrix
        self.Qmax = Qmax
        self.UAV_V = UAV_V
        self.n = len(customers)

    def calculate_cost(self, route):
        return sum(
            self.dist[route[i]][route[i + 1]]
            for i in range(len(route) - 1)
        )

    def build_random_route(self, depot, unvisited):

        route = [depot]
        capacity_left = self.Qmax
        current = depot

        while True:

            feasible = [
                c for c in unvisited
                if self.customers[c]["q"] <= capacity_left
            ]

            if not feasible:
                break

            nxt = random.choice(feasible)

            route.append(nxt)
            unvisited.remove(nxt)

            capacity_left -= self.customers[nxt]["q"]
            current = nxt

        route.append(depot)

        return route

    def run(self, trials=1000, depot=0):

        best_solution = None
        best_cost = float("inf")

        for _ in range(trials):

            unvisited = set(range(1, self.n))

            solution = []
            total_cost = 0

            while unvisited:

                route = self.build_random_route(
                    depot,
                    unvisited
                )

                solution.append(route)
                total_cost += self.calculate_cost(route)

            if total_cost < best_cost:
                best_cost = total_cost
                best_solution = solution

        return best_solution, best_cost