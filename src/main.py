from ga_only import GAOnly
from random_baseline import RandomBaseline
from aco_only import ACOOnly
from data.dataset import dataset_1, dataset_2, dataset_3, dataset_big, generate_random_dataset
from visualization import plot_solution, plot_convergence, plot_solution_compare


def run_experiment(name, customers, stops):
    print("\n======================")
    print("Dataset:", name)
    print("======================")

    ga = GAOnly(customers, stops)

    ga_best_solution, ga_best_cost, ga_open_stops, ga_assignments, ga_best_history = ga.run(max(50, min(200, 10 * len(stops))))

    print("Best solution:", ga_best_solution)
    print("Best cost:", ga_best_cost)

    rb = RandomBaseline(customers, stops)

    rb_solution, rb_cost, rb_open, rb_assign, rb_hist = rb.run(1000)
    print("Random baseline solution:", rb_solution)
    print("Random baseline cost:", rb_cost)
    # VISUALIZATION
    plot_solution(
        customers=customers,
        stops=stops,
        open_stops=ga_open_stops,
        assignments=ga_assignments
    )
    plot_convergence(ga_best_history)
    plot_solution_compare(
        customers=customers,
        stops=stops,
        ga_open=ga_open_stops,
        ga_assign=ga_assignments,
        rb_open=rb_open,
        rb_assign=rb_assign
    )


# run all datasets
datasets = [
    # ("Dataset 1", *dataset_1()),
    # ("Dataset 2", *dataset_2()),
    # ("Dataset 3", *dataset_3()),
    # ("Dataset Big", *dataset_big()),
    ("Random Dataset 1", *generate_random_dataset(num_customers=30, num_stops=8)),
    ("Random Dataset 2", *generate_random_dataset(num_customers=50, num_stops=12)),
    ("Random Dataset 3", *generate_random_dataset(num_customers=100, num_stops=15)),
    ("Random Dataset 4", *generate_random_dataset(num_customers=150, num_stops=20))
]

for name, customers, stops in datasets:
    run_experiment(name, customers, stops)