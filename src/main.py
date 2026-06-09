from ga_only import GAOnly
from data.dataset import dataset_1, dataset_2, dataset_3, dataset_big
from visualization import plot_solution


def run_experiment(name, customers, stops):
    print("\n======================")
    print("Dataset:", name)
    print("======================")

    ga = GAOnly(customers, stops)

    best_solution, best_cost, open_stops, assignments = ga.run(50)

    print("Best solution:", best_solution)
    print("Best cost:", best_cost)

    # -------------------------
    # VISUALIZATION (ADD THIS)
    # -------------------------
    plot_solution(
        customers=customers,
        stops=stops,
        open_stops=open_stops,
        assignments=assignments
    )


# run all datasets
datasets = [
    ("Dataset 1", *dataset_1()),
    ("Dataset 2", *dataset_2()),
    ("Dataset 3", *dataset_3()),
    ("Dataset Big", *dataset_big()),
]

for name, customers, stops in datasets:
    run_experiment(name, customers, stops)