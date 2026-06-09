def dataset_1():
    return (
        # simple balanced
        [
            {"id": 0, "x": 2, "y": 3},
            {"id": 1, "x": 5, "y": 4},
            {"id": 2, "x": 1, "y": 8},
            {"id": 3, "x": 7, "y": 2},
            {"id": 4, "x": 6, "y": 6},
        ],
        [
            {"id": 0, "x": 2, "y": 2},
            {"id": 1, "x": 6, "y": 3},
            {"id": 2, "x": 4, "y": 7},
        ]
    )


def dataset_2():
    return (
        # clustered + redundancy test
        [
            {"id": 0, "x": 1, "y": 2},
            {"id": 1, "x": 2, "y": 1},
            {"id": 2, "x": 2, "y": 3},
            {"id": 3, "x": 6, "y": 2},
            {"id": 4, "x": 7, "y": 3},
            {"id": 5, "x": 6, "y": 4},
            {"id": 6, "x": 3, "y": 8},
            {"id": 7, "x": 4, "y": 9},
        ],
        [
            {"id": 0, "x": 2, "y": 2},
            {"id": 1, "x": 6, "y": 3},
            {"id": 2, "x": 4, "y": 9},
            {"id": 3, "x": 8, "y": 7},
            {"id": 4, "x": 5, "y": 5},
        ]
    )


def dataset_3():
    return (
        # more spread (harder)
        [
            {"id": 0, "x": 1, "y": 1},
            {"id": 1, "x": 2, "y": 5},
            {"id": 2, "x": 3, "y": 8},
            {"id": 3, "x": 6, "y": 1},
            {"id": 4, "x": 7, "y": 4},
            {"id": 5, "x": 8, "y": 8},
            {"id": 6, "x": 5, "y": 6},
            {"id": 7, "x": 4, "y": 3},
            {"id": 8, "x": 9, "y": 2},
        ],
        [
            {"id": 0, "x": 1, "y": 1},
            {"id": 1, "x": 4, "y": 3},
            {"id": 2, "x": 6, "y": 1},
            {"id": 3, "x": 8, "y": 8},
            {"id": 4, "x": 3, "y": 8},
        ]
    )

def dataset_big():
    """
    Larger GA test dataset (15 customers, 7 stops)
    Designed for real clustering behavior
    """

    customers = [
        # Cluster 1 (bottom-left)
        {"id": 0, "x": 1, "y": 2},
        {"id": 1, "x": 2, "y": 1},
        {"id": 2, "x": 3, "y": 2},

        # Cluster 2 (center-left)
        {"id": 3, "x": 4, "y": 5},
        {"id": 4, "x": 5, "y": 4},
        {"id": 5, "x": 5, "y": 6},

        # Cluster 3 (center-right)
        {"id": 6, "x": 7, "y": 5},
        {"id": 7, "x": 8, "y": 4},
        {"id": 8, "x": 8, "y": 6},

        # Cluster 4 (top)
        {"id": 9, "x": 6, "y": 8},
        {"id": 10, "x": 7, "y": 9},
        {"id": 11, "x": 5, "y": 9},

        # Noise points
        {"id": 12, "x": 9, "y": 2},
        {"id": 13, "x": 2, "y": 8},
        {"id": 14, "x": 6, "y": 1},
    ]

    stops = [
        {"id": 0, "x": 2, "y": 2},   # cluster 1
        {"id": 1, "x": 5, "y": 5},   # center hub
        {"id": 2, "x": 8, "y": 5},   # cluster 3
        {"id": 3, "x": 6, "y": 9},   # top cluster
        {"id": 4, "x": 3, "y": 8},   # left-top
        {"id": 5, "x": 9, "y": 2},   # right-bottom
        {"id": 6, "x": 7, "y": 1},   # bottom-right
    ]

    return customers, stops

import random


def generate_random_dataset(num_customers, num_stops,
                             x_range=(0, 200), y_range=(0, 200),
                             seed=None):
    if seed is not None:
        random.seed(seed)

    customers = []
    stops = []

    # generate customers
    for i in range(num_customers):
        customers.append({
            "id": i,
            "x": random.randint(*x_range),
            "y": random.randint(*y_range)
        })

    # generate stops
    for i in range(num_stops):
        stops.append({
            "id": i,
            "x": random.randint(*x_range),
            "y": random.randint(*y_range)
        })

    return customers, stops