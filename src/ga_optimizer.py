import random
from aco_optimizer import ACO
from evaluator import evaluate_solution

class GA:
    def __init__(self, customers, stops, pop_size=10):
        self.customers = customers
        self.stops = stops
        self.pop_size = pop_size
        self.aco = ACO()

    def random_chromosome(self):
        stop_order = [s["id"] for s in self.stops]
        random.shuffle(stop_order)

        assignment = [random.randint(0, len(self.stops)-1)
                      for _ in self.customers]

        return (stop_order, assignment)

    def init_population(self):
        return [self.random_chromosome() for _ in range(self.pop_size)]

    def run(self, generations=20):
        pop = self.init_population()
        best = None
        best_fit = float("inf")

        for _ in range(generations):
            scored = []

            for chrom in pop:
                fit = evaluate_solution(chrom, self.customers, self.stops, self.aco)
                scored.append((fit, chrom))

                if fit < best_fit:
                    best_fit = fit
                    best = chrom

            scored.sort(key=lambda x: x[0])
            pop = [c for _, c in scored[:self.pop_size//2]]

            # crossover / mutation (simple)
            while len(pop) < self.pop_size:
                p1 = random.choice(pop)
                p2 = random.choice(pop)

                # --- better crossover (order preserved) ---
                child_order = p1[0][:]

                if random.random() < 0.5:
                    i, j = sorted(random.sample(range(len(child_order)), 2))
                    child_order[i:j] = p2[0][i:j]

                # --- better assignment crossover ---
                child_assign = []
                for a, b in zip(p1[1], p2[1]):
                    child_assign.append(a if random.random() < 0.5 else b)

                # --- stronger mutation ---
                if random.random() < 0.3:
                    i, j = random.sample(range(len(child_order)), 2)
                    child_order[i], child_order[j] = child_order[j], child_order[i]

                if random.random() < 0.4:
                    k = random.randint(0, len(child_assign)-1)
                    child_assign[k] = random.randint(0, len(self.stops)-1)

                # mutation
                if random.random() < 0.2:
                    i, j = random.sample(range(len(child_order)), 2)
                    child_order[i], child_order[j] = child_order[j], child_order[i]

                pop.append((child_order, child_assign))

        return best, best_fit