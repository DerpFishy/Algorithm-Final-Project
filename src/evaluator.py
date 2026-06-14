import numpy as np


class Evaluator:

    def __init__(
        self,
        stops,
        customers,
        customer_stop_matrix,
        max_distance=1,
        alpha=1
    ):
        self.stops = stops
        self.customers = customers
        self.customer_stop_matrix = customer_stop_matrix

        self.max_distance = max_distance
        self.alpha = alpha

    # penalty: number of open stops
    def stop_penalty(self, num_open):
        return self.alpha * np.sqrt(num_open)

    # distance penalty (vectorized logic)
    def distance_penalty(self, d):
        return np.where(
            d <= self.max_distance,
            0,
            (d - self.max_distance) * 10
        )

    # FITNESS (FAST VERSION)
    def evaluate(self, chrom):

        open_indices = np.flatnonzero(chrom)

        if len(open_indices) == 0:
            return float("inf")

        # distance matrix subset: (customers × open_stops)
        sub_matrix = self.customer_stop_matrix[:, open_indices]

        # nearest stop per customer
        nearest_dist = sub_matrix.min(axis=1)

        # cost per customer
        total_distance = np.mean(
            nearest_dist + self.distance_penalty(nearest_dist)
        )

        # facility cost
        facility_cost = self.stop_penalty(len(open_indices))

        # unused stop penalty (optional but kept from your logic)
        used = set(np.argmin(sub_matrix, axis=1))
        used_global = set(open_indices[i] for i in used)

        unused_open = len(open_indices) - len(used_global)
        unused_penalty = 5.0 * unused_open

        return total_distance + facility_cost + unused_penalty

    # VISUALIZATION (FAST + CORRECT)
    def assign(self, chrom):

        open_indices = np.flatnonzero(chrom)

        if len(open_indices) == 0:
            return [], []

        sub_matrix = self.customer_stop_matrix[:, open_indices]

        nearest_pos = np.argmin(sub_matrix, axis=1)

        assignments = [
            (
                self.customers[i],
                self.stops[open_indices[nearest_pos[i]]]
            )
            for i in range(len(self.customers))
        ]

        open_stops = [self.stops[i] for i in open_indices]

        return open_stops, assignments