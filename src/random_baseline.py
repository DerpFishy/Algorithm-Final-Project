import random
from evaluator import Evaluator


class RandomBaseline:

    def __init__(self, customers, stops):
        self.customers = customers
        self.stops = stops
        self.evaluator = Evaluator(stops, customers)

    def random_solution(self):
        return [random.randint(0, 1) for _ in self.stops]

    def run(self, iterations=100):

        best_solution = None
        best_cost = float("inf")

        history = []

        for i in range(iterations):

            chrom = self.random_solution()
            cost = self.evaluator.evaluate(chrom)

            history.append(cost)

            if cost < best_cost:
                best_cost = cost
                best_solution = chrom

        open_stops, assignments = self.evaluator.assign(best_solution)

        return best_solution, best_cost, open_stops, assignments, history