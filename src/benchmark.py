import numpy as np
from ga_optimizer import GA
from random_baseline import random_solution
from aco_optimizer import ACO
from data.dataset import generate_customers, generate_truck_stops

def run_benchmark(runs=20):
    ga_scores = []
    rand_scores = []
    ga_histories = []

    for seed in range(runs):
        customers = generate_customers(10, seed)
        stops = generate_truck_stops(3, seed)
        aco = ACO()

        ga = GA(customers, stops)
        (_, ga_score, hist) = ga.run()

        (_, rand_score) = random_solution(customers, stops, aco)

        ga_scores.append(ga_score)
        rand_scores.append(rand_score)
        ga_histories.append(hist)

    return ga_scores, rand_scores, ga_histories