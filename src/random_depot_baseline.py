import random

class RandomDepotBaseline:
    def __init__(self, depots, dist_matrix, V):
        self.depots = depots
        self.dist = dist_matrix
        self.V = V
        self.n = len(depots)

    def route_cost(self, route):
        return sum(
            self.dist[route[i]][route[i + 1]]
            for i in range(len(route) - 1)
        )

    def run(self, trials=1000):

        best_route = None
        best_cost = float("inf")

        for _ in range(trials):

            start = random.randrange(self.n)

            remaining = [i for i in range(self.n) if i != start]
            random.shuffle(remaining)

            route = [start] + remaining + [start]

            cost = self.route_cost(route)

            if cost < best_cost:
                best_cost = cost
                best_route = route

        return best_route, best_cost