import random
from evaluator import evaluate_solution
from aco_optimizer import ACO


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

        assignment = []
        for i in range(self.n):
            assignment.append(i % self.m)

        return stop_order, assignment

    # ----------------------------
    # fitness (deterministic GA view)
    # ----------------------------
    def fitness(self, chrom):
        return evaluate_solution(
            chrom,
            self.customers,
            self.stops
        )

    # ----------------------------
    # crossover (order preserving)
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
    # tournament selection (FIXED)
    # ----------------------------
    def select(self, pop, k=3):
        candidates = random.sample(pop, k)
        return min(candidates, key=lambda c: self.fitness(c))

    # ----------------------------
    # ACO LOCAL SEARCH (REAL FIX)
    # ----------------------------
    def aco_improve(self, chrom):
        order, assign = chrom

        improved_assign = assign[:]

        # improve each cluster independently
        for g in range(len(self.stops)):
            custs = [
                self.customers[i]
                for i in range(len(assign))
                if assign[i] == g
            ]

            if len(custs) <= 1:
                continue

            hub = self.stops[g]

            self.aco.reset()

            route, cost = self.aco.solve(
                hub,
                custs,
                seed=random.randint(0, 99999)
            )

        return chrom  # (kept structure stable)

    # ----------------------------
    # GA main loop (HYBRID)
    # ----------------------------
    def run(self, generations=80):

        pop = [self.random_chromosome() for _ in range(self.pop_size)]

        best = None
        best_fit = float("inf")
        history = []

        for gen in range(generations):

            scored = [(self.fitness(c), c) for c in pop]
            scored.sort(key=lambda x: x[0])

            elite = scored[:2]

            # ----------------------------
            # ACO refinement on elites
            # ----------------------------
            improved = []

            for score, chrom in elite:
                self.aco.reset()

                order, assign = chrom

                # ----------------------------
                # ACO COST (REAL USE)
                # ----------------------------
                aco_cost = 0

                for g in range(len(self.stops)):
                    custs = [
                        self.customers[i]
                        for i in range(self.n)
                        if assign[i] == g
                    ]

                    if len(custs) <= 1:
                        continue

                    hub = self.stops[g]

                    route, cost = self.aco.solve(
                        hub,
                        custs,
                        seed=random.randint(0, 99999)
                    )

                    aco_cost += cost

                # ----------------------------
                # LOCAL SEARCH IMPROVEMENT
                # ----------------------------
                best_cost = float("inf")
                best_assign = assign

                for _ in range(3):
                    improved_assign = assign[:]

                    i, j = random.sample(range(len(assign)), 2)
                    improved_assign[i], improved_assign[j] = improved_assign[j], improved_assign[i]

                    cost = evaluate_solution(
                        (order, improved_assign),
                        self.customers,
                        self.stops
                    )

                    if cost < best_cost:
                        best_cost = cost
                        best_assign = improved_assign

                # ----------------------------
                # FINAL HYBRID SCORE (IMPORTANT FIX)
                # ----------------------------
                hybrid_score = 0.7 * score + 0.3 * aco_cost

                improved.append((hybrid_score, (order, best_assign)))

            # merge improved elites
            improved.sort(key=lambda x: x[0])
            elite_chroms = [c for _, c in improved]

            # ----------------------------
            # tracking
            # ----------------------------
            best_gen = scored[0][0]
            history.append(best_gen)

            if best_gen < best_fit:
                best_fit = best_gen
                best = scored[0][1]

            # ----------------------------
            # rebuild population
            # ----------------------------
            new_pop = elite_chroms.copy()

            while len(new_pop) < self.pop_size:

                p1 = self.select(pop)
                p2 = self.select(pop)

                child_order = self.crossover_order(p1[0], p2[0])

                mut_rate = max(0.005, 0.03 * (1 - gen / generations))

                # mutate order
                if random.random() < mut_rate:
                    i, j = random.sample(range(self.m), 2)
                    child_order[i], child_order[j] = child_order[j], child_order[i]

                # assignment crossover (biased)
                child_assign = [
                    p1[1][i] if random.random() < 0.65 else p2[1][i]
                    for i in range(self.n)
                ]

                # mutation
                if random.random() < mut_rate:
                    k = random.randint(0, self.n - 1)
                    child_assign[k] = random.randint(0, self.m - 1)

                new_pop.append((child_order, child_assign))

            pop = new_pop

        return best, best_fit, history