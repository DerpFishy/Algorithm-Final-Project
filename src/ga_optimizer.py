import random
import math
from evaluator import evaluate_solution  # ONLY if deterministic version
from aco_optimizer import ACO


def dist(a, b):
    return math.hypot(a["x"] - b["x"], a["y"] - b["y"])


class GA:
    def __init__(self, customers, stops, pop_size=50):
        self.customers = customers
        self.stops = stops
        self.pop_size = pop_size

        self.m = len(stops)
        self.n = len(customers)

        self.aco = ACO()

    # ----------------------------
    # init chromosome
    # ----------------------------
    def random_chromosome(self):
        stop_order = list(range(self.m))
        random.shuffle(stop_order)

        assignment = [
            random.randint(0, self.m - 1)
            for _ in range(self.n)
        ]

        return stop_order, assignment

    # ----------------------------
    # deterministic fitness (NO ACO)
    # ----------------------------
    def fitness(self, chrom):
        return self.fast_evaluate(chrom)

    def fast_evaluate(self, chrom):
        order, assign = chrom
        cost = 0

        # assignment cost
        for i, c in enumerate(self.customers):
            s = self.stops[assign[i]]
            cost += dist(c, s)

        # route cost
        for i in range(len(order) - 1):
            a = self.stops[order[i]]
            b = self.stops[order[i + 1]]
            cost += dist(a, b)

        return cost

    # ----------------------------
    # crossover
    # ----------------------------
    def crossover_order(self, p1, p2):
        size = self.m
        a, b = sorted(random.sample(range(size), 2))

        child = [-1] * size
        child[a:b] = p1[a:b]

        fill = [x for x in p2 if x not in child]

        idx = 0
        for i in range(size):
            if child[i] == -1:
                child[i] = fill[idx]
                idx += 1

        return child

    # ----------------------------
    # GA main loop
    # ----------------------------
    def run(self, generations=50):

        pop = [self.random_chromosome() for _ in range(self.pop_size)]

        best = None
        best_fit = float("inf")
        history = []

        for gen in range(generations):

            scored = [(self.fitness(c), c) for c in pop]
            scored.sort(key=lambda x: x[0])

            elite = [scored[0][1], scored[1][1]]
            parents = [c for _, c in scored[:self.pop_size]]

            best_gen = scored[0][0]
            history.append(best_gen)

            if best_gen < best_fit:
                best_fit = best_gen
                best = scored[0][1]

            new_pop = elite.copy()

            while len(new_pop) < self.pop_size:

                p1 = random.choice(parents)
                p2 = random.choice(parents)

                child_order = self.crossover_order(p1[0], p2[0])

                mut_rate = max(0.05, 0.3 * (1 - gen / generations))

                # mutate order
                if random.random() < mut_rate:
                    i, j = random.sample(range(self.m), 2)
                    child_order[i], child_order[j] = child_order[j], child_order[i]

                # assignment crossover
                child_assign = [
                    p1[1][i] if random.random() < 0.5 else p2[1][i]
                    for i in range(self.n)
                ]

                # mutate assignment
                if random.random() < mut_rate:
                    k = random.randint(0, self.n - 1)
                    child_assign[k] = random.randint(0, self.m - 1)

                new_pop.append((child_order, child_assign))

            pop = new_pop

        return best, best_fit, history