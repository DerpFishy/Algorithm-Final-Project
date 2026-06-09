import math

class Constraints:

    def __init__(self, stops, customers=None, max_distance=8, alpha=5.0):
        self.stops = stops
        self.customers = customers
        self.max_distance = max_distance
        self.alpha = alpha

    # Euclidean distance
    def dist(self, a, b):
        return math.sqrt(
            (a["x"] - b["x"]) ** 2 +
            (a["y"] - b["y"]) ** 2
        )

    # penalty for number of open stops
    def stop_penalty(self, num_open_stops):
        return self.alpha * math.sqrt(num_open_stops)

    # smooth distance penalty
    def distance_penalty(self, min_dist):
        if min_dist <= self.max_distance:
            return 0

        # smooth penalty instead of hard jump
        return (min_dist - self.max_distance) * 10

    # evaluate one customer
    def evaluate_customer(self, customer, open_stops):

        # avoid crash when no stops are open
        if not open_stops:
            return float("inf")

        # compute nearest open stop
        min_dist = min(self.dist(customer, s) for s in open_stops)

        # apply soft penalty if too far
        penalty = self.distance_penalty(min_dist)

        return min_dist + penalty