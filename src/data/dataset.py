import random
import numpy as np


def generate_depot(seed=42):
    random.seed(seed)
    np.random.seed(seed)

    return {
        "id": 0,
        "x": random.randint(0, 100),
        "y": random.randint(0, 100)
    }


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
    random.seed(seed + 100)  # avoid identical overlap with customers

    stops = []
    for i in range(n):
        stops.append({
            "id": i,
            "x": random.randint(0, 100),
            "y": random.randint(0, 100)
        })
    return stops


def generate_instance(n_customers=10, n_stops=3, seed=42):
    random.seed(seed)
    np.random.seed(seed)

    return {
        "depot": generate_depot(),
        "customers": generate_customers(n_customers),
        "stops": generate_truck_stops(n_stops)
    }