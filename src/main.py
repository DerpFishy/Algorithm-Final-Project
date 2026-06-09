from ga_only import GAOnly
from random_baseline import RandomBaseline
from aco_only import ACOOnly
from depot_aco import DepotACO
from helper import build_clusters, build_distance_matrix_np, build_customer_stop_matrix
from data.dataset import generate_random_dataset
from visualization import plot_solution, plot_convergence, plot_solution_compare, plot_all_aco_routes

def run_experiment(name, customers, stops, Qmax, V):
    print("\n======================")
    print("Dataset:", name)
    print("======================")

    customer_stop_matrix = build_customer_stop_matrix(customers, stops)

    ga = GAOnly(customers, stops, customer_stop_matrix)

    ga_best_solution, ga_best_cost, ga_open_stops, ga_assignments, ga_best_history = ga.run(max(50, min(200, 10 * len(stops))))

    print("Best solution:", ga_best_solution)
    print("Best cost:", ga_best_cost)

    rb = RandomBaseline(customers, stops, customer_stop_matrix)

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

    depots = ga_open_stops
    depot_matrix = build_distance_matrix_np(depots)

    truck_aco = DepotACO(depots, depot_matrix)
    best_depot_route, truck_cost = truck_aco.run()

    aco_results = {}
    aco_total_cost = 0

    clusters = build_clusters(ga_assignments)

    # keep full nodes for final plot
    all_customers_for_plot = []
    all_stops_for_plot = stops

    for stop_id, data in clusters.items():

        stop = data["stop"]
        cluster_customers = data["customers"]

        customers_for_aco = [stop] + cluster_customers

        distance_matrix = build_distance_matrix_np(customers_for_aco)

        aco = ACOOnly(
            customers=customers_for_aco,
            distance_matrix=distance_matrix,
            Qmax=Qmax,
            V=V
        )

        best_routes, best_cost = aco.run()

        aco_results[stop_id] = {
            "stop": stop,
            "nodes": customers_for_aco,
            "routes": best_routes,
            "cost": best_cost
        }

        # store for global plotting
        all_customers_for_plot = customers
        aco_total_cost += best_cost

    print("Truck route:", best_depot_route)
    print("Truck route cost:", truck_cost)
    print("Total ACO cost:", aco_total_cost)
    plot_all_aco_routes(
        customers=all_customers_for_plot,
        stops=all_stops_for_plot,
        aco_results=aco_results,
        depot_route=best_depot_route,
        chrom=ga_best_solution
    )

# run all datasets
datasets = [
    ("Random Dataset 1", *generate_random_dataset(num_customers=100, num_stops=25, seed = 1)),
    ("Random Dataset 2", *generate_random_dataset(num_customers=200, num_stops=25, seed = 2)),
    ("Random Dataset 3", *generate_random_dataset(num_customers=200, num_stops=40, seed = 3)),
    ("Random Dataset 4", *generate_random_dataset(num_customers=200, num_stops=55, seed = 4)),
]

for name, customers, stops, Qmax, V in datasets:
    run_experiment(name, customers, stops, Qmax, V)