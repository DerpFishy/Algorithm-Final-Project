def build_clusters(assignments):
    clusters = {}

    for customer, stop in assignments:
        sid = stop["id"]

        if sid not in clusters:
            clusters[sid] = {
                "stop": stop,
                "customers": []
            }

        clusters[sid]["customers"].append(customer)

    return clusters

import math
import numpy as np

# Euclidean distance
def dist(a, b):
    return math.sqrt(
        (a["x"] - b["x"]) ** 2 +
        (a["y"] - b["y"]) ** 2
    )

# Build distance matrix
def build_distance_matrix_np(nodes):
    coords = np.array([[n["x"], n["y"]] for n in nodes])

    diff = coords[:, None, :] - coords[None, :, :]
    return np.sqrt((diff ** 2).sum(axis=2))

def build_customer_stop_matrix(customers, stops):

    c = np.array([[x["x"], x["y"]] for x in customers])
    s = np.array([[x["x"], x["y"]] for x in stops])

    diff = c[:, None, :] - s[None, :, :]

    return np.sqrt((diff ** 2).sum(axis=2))