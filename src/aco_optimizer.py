import random
import math


def dist(a, b):
    return math.hypot(a["x"] - b["x"], a["y"] - b["y"])


class ACO:
    def __init__(self, beta=2, iters=20):
        self.beta = beta
        self.iters = iters
        self.pheromone = {}

    # ✅ IMPORTANT: called every GA evaluation
    def reset(self, seed=None):
        if seed is not None:
            import random
            random.seed(seed)

        # also reset internal ACO state here
        self.pheromone = { }
        self.best = None

    def solve(self, depot, customers, seed=None):
        if len(customers) == 0:
            return [], 0

        if seed is not None:
            random.seed(seed)

        best_cost = float("inf")
        best_route = None

        for _ in range(self.iters):
            unvisited = customers[:]
            current = depot
            route = []
            cost = 0

            while unvisited:
                probs = []

                for c in unvisited:
                    d = dist(current, c)
                    key = (current["id"], c["id"])
                    pher = self.pheromone.get(key, 1.0)

                    probs.append(pher * (1.0 / (d + 1e-6)) ** self.beta)

                total = sum(probs)
                probs = [p / total for p in probs]

                choice = random.choices(unvisited, weights=probs, k=1)[0]

                cost += dist(current, choice)
                route.append(choice)
                current = choice
                unvisited.remove(choice)

            cost += dist(current, depot)

            if cost < best_cost:
                best_cost = cost
                best_route = route

                # pheromone update (stable)
                for i in range(len(route) - 1):
                    a = route[i]["id"]
                    b = route[i + 1]["id"]
                    self.pheromone[(a, b)] = self.pheromone.get((a, b), 0) + 1.0 / (cost + 1e-6)

        return best_route, best_cost