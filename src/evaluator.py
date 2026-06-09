import math
from constraint import Constraints


class Evaluator:

    def __init__(self, stops, customers, max_distance=8, alpha=3.0):
        self.stops = stops
        self.customers = customers
        self.constraints = Constraints(stops, max_distance, alpha)

    # ----------------------------
    # use ONE source of distance
    # ----------------------------
    def dist(self, a, b):
        return self.constraints.dist(a, b)

    # ----------------------------
    # fitness function
    # ----------------------------
    def evaluate(self, chrom):

        open_stops = [
            self.stops[i]
            for i in range(len(chrom))
            if chrom[i] == 1
        ]

        # invalid solution
        if not open_stops:
            return float("inf")

        distance_cost = 0

        for c in self.customers:
            distance_cost += self.constraints.evaluate_customer(c, open_stops)

        distance_cost = distance_cost / len(self.customers)

        facility_cost = self.constraints.stop_penalty(len(open_stops))

        total_cost = distance_cost + facility_cost
        return total_cost

    # ----------------------------
    # for visualization only
    # ----------------------------
    def assign(self, chrom):

        open_stops = [
            self.stops[i]
            for i in range(len(chrom))
            if chrom[i] == 1
        ]

        if not open_stops:
            return [], []

        assignments = []

        for c in self.customers:
            best_stop = min(
                open_stops,
                key=lambda s: self.constraints.dist(c, s)
            )

            assignments.append((c, best_stop))

        return open_stops, assignments