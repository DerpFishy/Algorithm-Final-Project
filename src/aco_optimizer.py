import random
import math

def dist(a, b):
    return math.hypot(a["x"] - b["x"], a["y"] - b["y"])


class ACO:
    def __init__(self, alpha=1, beta=2, iters=30):
        self.alpha = alpha
        self.beta = beta
        self.iters = iters
        self.pheromone = {}

    def solve(self, depot, customers):
        if len(customers) == 0:
            return [], 0

        best_route = None
        best_cost = float("inf")

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
                    pheromone = self.pheromone.get(key, 1.0)
                    prob = pheromone * (1 / (d + 1e-6)) ** self.beta
                    probs.append(prob)

                total = sum(probs)
                probs = [p / total for p in probs]

                choice = random.choices(unvisited, weights=probs)[0]

                cost += dist(current, choice)
                route.append(choice)
                current = choice
                unvisited.remove(choice)

            cost += dist(current, depot)

            if cost < best_cost:
                best_cost = cost
                best_route = route
                for i in range(len(route) - 1):
                    a = route[i]["id"]
                    b = route[i+1]["id"]
                    self.pheromone[(a, b)] = self.pheromone.get((a, b), 0) + 1.0 / (cost + 1e-6)

        return best_route, best_cost