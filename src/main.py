from dataset import generate_customers, generate_truck_stops
from ga_optimizer import GA
from random_baseline import random_solution
from visualization import plot_side_by_side, plot_bar_comparison
from aco_optimizer import ACO
from benchmark import run_benchmark
import numpy as np

def main():
    customers = generate_customers(10)
    stops = generate_truck_stops(3)

    aco = ACO()

    # single run comparison
    ga = GA(customers, stops)
    ga_sol, ga_score = ga.run()

    rand_sol, rand_score = random_solution(customers, stops, aco)

    print("\n===== SINGLE RUN =====")
    print("GA Score     :", ga_score)
    print("Random Score :", rand_score)

    # VISUAL 1: side-by-side routes
    plot_side_by_side(customers, stops, ga_sol, rand_sol)

    # VISUAL 2: bar chart
    plot_bar_comparison(ga_score, rand_score)

    # VISUAL 3: benchmark stats
    print("\n===== BENCHMARK (20 runs) =====")

    ga_scores, rand_scores = run_benchmark(20)

    print("GA Avg     :", np.mean(ga_scores))
    print("Random Avg :", np.mean(rand_scores))
    print("GA Std     :", np.std(ga_scores))
    print("Random Std :", np.std(rand_scores))


if __name__ == "__main__":
    main()