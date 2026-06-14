import random
from evaluator import Evaluator


class GAOnly:

    def __init__(self, customers, stops, customer_stop_matrix):
        self.customers = customers
        self.stops = stops
        self.customer_stop_matrix = customer_stop_matrix
        self.pop_size = max(30, min(500, 10 * len(stops)))
        self.elite_size = max(2, self.pop_size // 10)

        # stronger constraint pressure
        self.evaluator = Evaluator(stops, customers, customer_stop_matrix)

    # INIT
    def random_chromosome(self):
        return [random.randint(0, 1) for _ in self.stops]

    # FITNESS
    def fitness(self, chrom):
        return self.evaluator.evaluate(chrom)

    # TOURNAMENT SELECTION
    def tournament_selection(self, population, fitness_vals, k=5):
        selected = []

        for _ in range(len(population)):
            candidates = random.sample(list(zip(population, fitness_vals)), k)
            winner = min(candidates, key=lambda x: x[1])
            selected.append(winner[0])

        return selected

    # CROSSOVER
    def crossover(self, p1, p2):
        return [
            p1[i] if random.random() < 0.5 else p2[i]
            for i in range(len(p1))
        ]

    # MUTATION
    def mutation(self, chrom, rate=0.3):
        for i in range(len(chrom)):
            if random.random() < rate:
                chrom[i] ^= 1

        # ensure validity
        if sum(chrom) == 0:
            chrom[random.randint(0, len(chrom) - 1)] = 1

        return chrom

    # GET BEST
    def get_best(self, population):
        fitness_vals = [self.fitness(c) for c in population]
        best_idx = fitness_vals.index(min(fitness_vals))
        return population[best_idx], fitness_vals[best_idx]

    # RUN GA
    def run(self, generations):

        # init population
        population = [self.random_chromosome() for _ in range(self.pop_size)]

        best_solution = None
        best_cost = float("inf")
        best_history = []

        for gen in range(generations):

            fitness_vals = [self.fitness(c) for c in population]

            # track global best
            gen_best_idx = fitness_vals.index(min(fitness_vals))
            if fitness_vals[gen_best_idx] < best_cost:
                best_cost = fitness_vals[gen_best_idx]
                best_solution = population[gen_best_idx]

            # print(f"Gen {gen} best cost: {fitness_vals[gen_best_idx]}")
            best_history.append(fitness_vals[gen_best_idx])

            # ELITISM (KEEP BEST)
            sorted_pop = sorted(
                zip(population, fitness_vals),
                key=lambda x: x[1]
            )

            new_pop = [ind[0] for ind in sorted_pop[:self.elite_size]]

            # SELECTION
            selected = self.tournament_selection(population, fitness_vals)

            # CROSSOVER + MUTATION
            while len(new_pop) < self.pop_size:

                p1 = random.choice(selected)
                p2 = random.choice(selected)

                child = self.crossover(p1, p2)
                child = self.mutation(child)

                new_pop.append(child)

            # DIVERSITY INJECTION to prevent stagnation
            for i in range(self.elite_size, self.elite_size + 2):
                if i < len(new_pop) and random.random() < 0.1:
                    new_pop[i] = self.random_chromosome()

            population = new_pop

        # FINAL RESULT
        open_stops, assignments = self.evaluator.assign(best_solution)

        return best_solution, best_cost, open_stops, assignments, best_history