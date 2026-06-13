import math
import random

class ACOOnly:
    def __init__(self, customers, distance_matrix, Qmax, UAV_V,
                 n_ants=10,
                 alpha=1.5,
                 beta=1.5,
                 rho=0.2):

        self.customers = customers
        self.dist = distance_matrix
        self.Qmax = Qmax
        self.UAV_V = UAV_V

        self.n_ants = n_ants
        self.alpha = alpha
        self.beta = beta
        self.rho = rho

        self.n = len(customers)

        # pheromone matrix
        self.pheromone = [[1.0 for _ in range(self.n)] for _ in range(self.n)]

        self.best_history = []
        self.avg_history = []

    # cost
    def calculate_cost(self, route):
        return sum(self.dist[route[i]][route[i + 1]]
                   for i in range(len(route) - 1))

    # heuristic
    def heuristic(self, i, j):
        return 1.0 / (self.dist[i][j] + 1e-9)

    # probability-based selection (REAL ACO CORE)
    def choose_next(self, current, unvisited, capacity_left):

        feasible = [
            j for j in unvisited
            if self.customers[j]["q"] <= capacity_left
        ]

        if not feasible:
            return None

        # exploration
        if random.random() < 0.1:
            return random.choice(feasible)

        # ACO probability
        probs = []
        total = 0.0

        for j in feasible:
            tau = self.pheromone[current][j] ** self.alpha
            eta = self.heuristic(current, j) ** self.beta
            score = tau * eta
            probs.append((j, score))
            total += score

        # normalize + roulette wheel
        r = random.random()
        cum = 0.0

        for j, score in probs:
            cum += score / (total + 1e-9)
            if r <= cum:
                return j

        return feasible[-1]

    # build ONE route (depot → customers → depot)
    def build_route(self, depot, unvisited):

        route = [depot]
        capacity = self.Qmax
        current = depot

        while True:

            nxt = self.choose_next(current, unvisited, capacity)

            if nxt is None:
                break

            route.append(nxt)
            unvisited.remove(nxt)
            capacity -= self.customers[nxt]["q"]

            current = nxt

        route.append(depot)
        return route

    # pheromone update
    def update_pheromone(self, all_routes, costs):

        # evaporation
        for i in range(self.n):
            for j in range(self.n):
                self.pheromone[i][j] *= (1 - self.rho)

        # best ants only
        k = max(1, len(costs) // 5)
        ranked = sorted(zip(all_routes, costs), key=lambda x: x[1])[:k]

        for solution, cost in ranked:
            deposit = 1.0 / (cost + 1e-9)

            for route in solution:
                for i in range(len(route) - 1):
                    a, b = route[i], route[i + 1]
                    self.pheromone[a][b] += deposit
                    self.pheromone[b][a] += deposit

    # main run
    def run(self, iterations=50, depot=0):

        best_solution = None
        best_cost = float("inf")

        for it in range(iterations):

            all_solutions = []
            costs = []

            for _ in range(self.n_ants):

                unvisited = set(range(1, self.n))
                solution = []
                total_cost = 0

                while unvisited:
                    route = self.build_route(depot, unvisited)
                    solution.append(route)
                    total_cost += self.calculate_cost(route)

                all_solutions.append(solution)
                costs.append(total_cost)

                if total_cost < best_cost:
                    best_cost = total_cost
                    best_solution = solution

            self.update_pheromone(all_solutions, costs)

            self.best_history.append(best_cost)
            self.avg_history.append(sum(costs) / len(costs))

            # print(f"Iter {it+1}: Best={best_cost:.4f}, Avg={self.avg_history[-1]:.4f}")

        return best_solution, best_cost