from data.dataset import generate_customers, generate_truck_stops
from ga_optimizer import GA
from random_baseline import random_solution
from aco_optimizer import ACO

from benchmark import run_benchmark

# 📊 statistical + evaluation plots
from evaluation_viz import (
    plot_convergence,
    plot_boxplot,
    plot_bar,
    run_ttest
)

# 🗺️ route visualization
from visualization import plot_side_by_side

import numpy as np


def main():

    # =========================
    # SINGLE RUN (for convergence + route view)
    # =========================
    customers = generate_customers(10)
    stops = generate_truck_stops(3)
    aco = ACO()

    ga = GA(customers, stops)

    ga_solution, ga_score, history = ga.run()
    rand_solution, rand_score = random_solution(customers, stops, aco)

    print("\n===== SINGLE RUN =====")
    print("GA Score     :", ga_score)
    print("Random Score :", rand_score)

    # 🗺️ VISUALIZATION 1: route comparison
    plot_side_by_side(customers, stops, ga_solution, rand_solution)

    # 📈 VISUALIZATION 2: GA convergence
    plot_convergence(history)

    # =========================
    # MULTI RUN BENCHMARK
    # =========================
    ga_scores, rand_scores, _ = run_benchmark(20)

    print("\n===== BENCHMARK (20 runs) =====")
    print("GA Avg     :", np.mean(ga_scores))
    print("Random Avg :", np.mean(rand_scores))
    print("GA Std     :", np.std(ga_scores))
    print("Random Std :", np.std(rand_scores))

    # 📊 VISUALIZATION 3: boxplot
    plot_boxplot(ga_scores, rand_scores)

    # 📊 VISUALIZATION 4: bar chart
    plot_bar(ga_scores, rand_scores)

    # 🧪 statistical test
    run_ttest(ga_scores, rand_scores)


if __name__ == "__main__":
    main()