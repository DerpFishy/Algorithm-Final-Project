# Algorithm 1: Genetic Algorithm (GA Only)

# Input:
#     Customers C
#     Candidate Stops S
#     Population size P
#     Generations G

# Output:
#     Best solution (stop selection + assignment)

# Begin

#     Initialize population P randomly:
#         Each chromosome = (y_s, x_i^s)
#         y_s ∈ {0,1}  // stop selection
#         x_i^s ∈ ordered set of selected stops

#     For generation = 1 to G do:

#         For each chromosome in P:
#             fitness = CostFunction(chromosome)
#         End

#         Preserve E elite individuals into P_new

#         While P_new not full do:
#             Parent1 = TournamentSelection(P)
#             Parent2 = TournamentSelection(P)

#             Child = UniformCrossover(Parent1, Parent2)

#             Child = Mutation(Child):
#                 Flip y_s with probability pm
#                 Modify x_i^s while maintaining feasibility

#             Add Child to P_new
#         End

#         P = P_new

#     End For

#     Return best chromosome in P

# End

# Initialize population
# Evaluate fitness
# Selection
# Crossover
# Mutation
# Repeat
# Return best

import random
import math

from evaluator import Evaluator


class GAOnly:

    def __init__(self, customers, stops, pop_size=50):
        self.customers = customers
        self.stops = stops
        self.n = len(customers)
        self.m = len(stops)
        self.pop_size = pop_size
        self.evaluator = Evaluator(stops, customers, alpha=3.0)

    # chromosomen for stop selection only
    def random_chromosome(self):
        return [random.randint(0, 1) for _ in self.stops]

    # fitness
    def fitness(self, chrom):
        return self.evaluator.evaluate(chrom)

    # selection
    def tournament_selection(self, population, fitness, k=3):
        selected = []

        for _ in range(len(population)):
            candidates = random.sample(list(zip(population, fitness)), k)
            winner = min(candidates, key=lambda x: x[1])
            selected.append(winner[0])

        return selected

    # crossover
    def crossover(self, p1, p2):
        child = []

        for i in range(len(p1)):
            child.append(p1[i] if random.random() < 0.5 else p2[i])

        return child
    
    # mutation (flip stop open/close)
    def mutation(self, chrom, rate=0.2):
        for i in range(len(chrom)):
            if random.random() < rate:
                chrom[i] = 1 - chrom[i]

        # ensure at least one stop is open
        if sum(chrom) == 0:
            chrom[random.randint(0, len(chrom)-1)] = 1

        return chrom
    
    # run GA
    def run(self, generations=50):

        population = [self.random_chromosome() for _ in range(self.pop_size)]

        for gen in range(generations):

            fitness_vals = [self.fitness(c) for c in population]

            best_idx = fitness_vals.index(min(fitness_vals))
            print(f"Gen {gen} best cost: {fitness_vals[best_idx]}")

            # selection
            population = self.tournament_selection(population, fitness_vals)

            # crossover + mutation
            new_pop = []

            for i in range(0, len(population), 2):
                p1 = population[i]
                p2 = population[(i+1) % len(population)]

                c1 = self.crossover(p1, p2)
                c2 = self.crossover(p2, p1)

                new_pop.append(self.mutation(c1))
                new_pop.append(self.mutation(c2))

            population = new_pop

        final_fitness = [self.fitness(c) for c in population]
        best_idx = final_fitness.index(min(final_fitness))

        best_solution = population[best_idx]
        best_cost = final_fitness[best_idx]

        open_stops, assignments = self.evaluator.assign(best_solution)

        return best_solution, best_cost, open_stops, assignments