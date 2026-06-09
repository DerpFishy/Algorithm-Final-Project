import numpy as np

class Constraints:

    def __init__(self, max_distance, alpha=1500.0):
        self.max_distance = max_distance
        self.alpha = alpha

    # penalty for number of open stops
    def stop_penalty(self, num_open_stops):
        return self.alpha * np.sqrt(num_open_stops)

    # vectorized distance penalty
    def distance_penalty(self, dist_array):
        return np.where(
            dist_array <= self.max_distance,
            0,
            (dist_array - self.max_distance) * 10
        )