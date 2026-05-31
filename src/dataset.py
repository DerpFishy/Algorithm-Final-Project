import random
import numpy as np

def generate_customers(n=10, seed=42):
    random.seed(seed)
    np.random.seed(seed)

    customers = []
    for i in range(n):
        customers.append({
            "id": i,
            "x": random.randint(0, 100),
            "y": random.randint(0, 100),
            "demand": random.randint(1, 5)
        })
    return customers


def generate_truck_stops(n=3, seed=42):
    random.seed(seed)

    stops = []
    for i in range(n):
        stops.append({
            "id": i,
            "x": random.randint(0, 100),
            "y": random.randint(0, 100),
        })
    return stops