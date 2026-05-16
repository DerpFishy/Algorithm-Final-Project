import numpy as np

def generate_data(num_customers):

    np.random.seed(42)

    # Depot + customers
    locations = np.random.rand(num_customers + 1, 2) * 100

    # Customer demands
    demands = np.random.randint(1, 6, num_customers + 1)
    demands[0] = 0

    return locations, demands


def create_distance_matrix(locations):

    size = len(locations)

    matrix = np.zeros((size, size))

    for i in range(size):
        for j in range(size):

            matrix[i][j] = np.linalg.norm(
                locations[i] - locations[j]
            )

    return matrix