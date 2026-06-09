import random

class DepotACO:
    def __init__(self, depots, dist_matrix, n_ants=10, alpha=2, beta=1, rho=0.2):

        self.depots = depots
        self.dist = dist_matrix

        self.n = len(depots)

        self.n_ants = n_ants
        self.alpha = alpha
        self.beta = beta
        self.rho = rho

        self.pheromone = [[1.0]*self.n for _ in range(self.n)]

    def heuristic(self, i, j):
        return 1.0 / (self.dist[i][j] + 1e-9)

    def choose_next(self, current, unvisited):

        candidates = list(unvisited)
        if not candidates:
            return None

        probs = []
        total = 0

        for j in candidates:
            score = (self.pheromone[current][j] ** self.alpha) * \
                    (self.heuristic(current, j) ** self.beta)
            probs.append((j, score))
            total += score

        r = random.random()
        cum = 0

        for j, score in probs:
            cum += score / (total + 1e-9)
            if r <= cum:
                return j

        return candidates[-1]

    def run(self, iterations=50):

        best_route = None
        best_cost = float("inf")

        for _ in range(iterations):

            all_routes = []
            costs = []

            for _ in range(self.n_ants):

                unvisited = set(range(self.n))
                start = random.choice(range(self.n))
                current = start
                route = [start]
                unvisited.remove(current)

                while unvisited:
                    nxt = self.choose_next(current, unvisited)
                    if nxt is None:
                        break

                    route.append(nxt)
                    unvisited.remove(nxt)
                    current = nxt

                route.append(start)

                cost = sum(self.dist[route[i]][route[i+1]]
                           for i in range(len(route)-1))

                all_routes.append(route)
                costs.append(cost)

                if cost < best_cost:
                    best_cost = cost
                    best_route = route

            # pheromone update
            for i in range(self.n):
                for j in range(self.n):
                    self.pheromone[i][j] *= (1 - self.rho)

            for route, cost in zip(all_routes, costs):
                for i in range(len(route)-1):
                    a, b = route[i], route[i+1]
                    self.pheromone[a][b] += 1.0 / (cost + 1e-9)

        return best_route, best_cost