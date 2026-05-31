from ga_optimizer import GA
from random_baseline import random_solution
from aco_optimizer import ACO
from dataset import generate_customers, generate_truck_stops

def run_benchmark(runs=20):
    ga_scores = []
    rand_scores = []

    for seed in range(runs):
        customers = generate_customers(10, seed)
        stops = generate_truck_stops(3, seed)
        aco = ACO()

        # GA
        ga = GA(customers, stops)
        _, ga_score = ga.run()

        # Random
        _, rand_score = random_solution(customers, stops, aco)

        ga_scores.append(ga_score)
        rand_scores.append(rand_score)

    return ga_scores, rand_scores