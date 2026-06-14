from ga_only import GAOnly
from random_selection_baseline import RandomSelectionBaseline
from random_depot_baseline import RandomDepotBaseline
from random_uav_baseline import RandomUAVBaseline
from aco_only import ACOOnly
from depot_aco import DepotACO
from helper import build_clusters, build_distance_matrix_np, build_customer_stop_matrix
from data.dataset import generate_random_dataset
from visualization import plot_convergence, plot_solution_compare, plot_all_routes, plot_bar_comparison

def run_experiment(name, customers, stops, Qmax, truck_V, UAV_V):
    print("\n======================")
    print("Dataset:", name)
    print("======================")

    customer_stop_matrix = build_customer_stop_matrix(customers, stops)

    rsb = RandomSelectionBaseline(customers, stops, customer_stop_matrix)

    rsb_solution, rsb_cost, rsb_open, rsb_assign, rsb_hist = rsb.run(min(100000, 15 * len(customers) * len(stops)))
    rsb_cost = round(rsb_cost, 2)
    print("RSB solution:", rsb_solution)
    print("RSB cost:", rsb_cost)

    ga = GAOnly(customers, stops, customer_stop_matrix)
    ga_best_solution, ga_best_cost, ga_open_stops, ga_assignments, ga_best_history = ga.run(min(400, 15 * len(stops)))
    ga_best_cost = round(ga_best_cost, 2)

    print("Best solution:", ga_best_solution)
    print("Best cost:", ga_best_cost)
    # VISUALIZATION
    plot_convergence(ga_best_history)
    plot_solution_compare(
        customers=customers,
        stops=stops,
        ga_open=ga_open_stops,
        ga_assign=ga_assignments,
        rsb_open=rsb_open,
        rsb_assign=rsb_assign
    )

    ga_depots = ga_open_stops
    ga_depot_matrix = build_distance_matrix_np(ga_depots)
    rsb_depot_matrix = build_distance_matrix_np(rsb_open)
    
    trdb = RandomDepotBaseline(rsb_open, rsb_depot_matrix, truck_V)
    trdb_truck_depot_route, trdb_truck_cost = trdb.run((len(rsb_open) ** 2) * 10)
    trdb_truck_cost /= truck_V  # convert to time
    print("TRDB Truck route:", trdb_truck_depot_route)
    print("TRDB Truck route cost:", trdb_truck_cost)

    random_aco = DepotACO(rsb_open, rsb_depot_matrix, truck_V)
    random_aco_truck_depot_route, random_aco_truck_cost = random_aco.run()
    random_aco_truck_cost /= truck_V  # convert to time
    print("Random ACO Truck route:", random_aco_truck_depot_route)
    print("Random ACO Truck route cost:", random_aco_truck_cost)

    ga_rdb = RandomDepotBaseline(ga_depots, ga_depot_matrix, truck_V)
    ga_rdb_truck_depot_route, ga_rdb_truck_cost = ga_rdb.run((len(ga_depots) ** 2) * 10)
    ga_rdb_truck_cost /= truck_V  # convert to time
    print("GA RDB Truck route:", ga_rdb_truck_depot_route)
    print("GA RDB Truck route cost:", ga_rdb_truck_cost)

    hybrid_truck = DepotACO(ga_depots, ga_depot_matrix, truck_V)
    hybrid_truck_depot_route, hybrid_truck_cost = hybrid_truck.run()
    hybrid_truck_cost /= truck_V  # convert to time
    print("Hybrid Truck route:", hybrid_truck_depot_route)
    print("Hybrid Truck route cost:", hybrid_truck_cost)

    rsb_clusters = build_clusters(rsb_assign)
    ga_clusters = build_clusters(ga_assignments)

    # True Random (random clusters + random routes)
    trandom_results = {}
    trandom_total_cost = 0
    all_trandom_customers_for_plot = []
    for stop_id, data in rsb_clusters.items():

        stop = data["stop"]
        cluster_customers = data["customers"]

        customers_for_random = [stop] + cluster_customers

        distance_matrix = build_distance_matrix_np(customers_for_random)

        trandom_uav = RandomUAVBaseline(
            customers=customers_for_random,
            distance_matrix=distance_matrix,
            Qmax=Qmax,
            UAV_V=UAV_V
        )

        trandom_best_routes, trandom_best_cost = trandom_uav.run()

        trandom_results[stop_id] = {
            "stop": stop,
            "nodes": customers_for_random,
            "routes": trandom_best_routes,
            "cost": trandom_best_cost
        }
        all_trandom_customers_for_plot = customers
        trandom_total_cost += trandom_best_cost

    trandom_total_cost /= UAV_V  # convert to time
    trandom_total_cost += trdb_truck_cost  # add truck time

    print("Total True Random cost:", round(trandom_total_cost, 2))
    plot_all_routes(
        customers=all_trandom_customers_for_plot,
        stops=stops,
        results=trandom_results,
        depot_route=trdb_truck_depot_route,
        chrom=rsb_solution,
        plotTitle="True Random: Random Clusters + Random Routes"
    )

    # Random Clusters + ACO Routes
    random_aco_results = {}
    random_aco_total_cost = 0
    all_random_aco_customers_for_plot = []

    for stop_id, data in rsb_clusters.items():

        stop = data["stop"]
        rsb_cluster_customers = data["customers"]

        customers_for_random_aco = [stop] + rsb_cluster_customers

        distance_matrix = build_distance_matrix_np(customers_for_random_aco)

        random_aco = ACOOnly(
            customers=customers_for_random_aco,
            distance_matrix=distance_matrix,
            Qmax=Qmax,
            UAV_V=UAV_V
        )

        random_aco_best_routes, random_aco_best_cost = random_aco.run()

        random_aco_results[stop_id] = {
            "stop": stop,
            "nodes": customers_for_random_aco,
            "routes": random_aco_best_routes,
            "cost": random_aco_best_cost
        }

        # store for global plotting
        all_random_aco_customers_for_plot = customers
        random_aco_total_cost += random_aco_best_cost

    random_aco_total_cost /= UAV_V  # convert to time
    random_aco_total_cost += random_aco_truck_cost  # add truck time

    print("Total Random ACO cost:", round(random_aco_total_cost, 2))
    plot_all_routes(
        customers=all_random_aco_customers_for_plot,
        stops=stops,
        results=random_aco_results,
        depot_route=random_aco_truck_depot_route,
        chrom=rsb_solution,
        plotTitle="Random Clusters + ACO Routes"
    )

    # GA Clusters + Random Routes
    ga_random_results = {}
    ga_random_total_cost = 0
    all_ga_random_customers_for_plot = []
    for stop_id, data in ga_clusters.items():

        stop = data["stop"]
        ga_cluster_customers = data["customers"]

        customers_for_ga_random = [stop] + ga_cluster_customers

        distance_matrix = build_distance_matrix_np(customers_for_ga_random)

        ga_random_uav = RandomUAVBaseline(
            customers=customers_for_ga_random,
            distance_matrix=distance_matrix,
            Qmax=Qmax,
            UAV_V=UAV_V
        )

        ga_random_best_routes, ga_random_best_cost = ga_random_uav.run()

        ga_random_results[stop_id] = {
            "stop": stop,
            "nodes": customers_for_ga_random,
            "routes": ga_random_best_routes,
            "cost": ga_random_best_cost
        }
        all_ga_random_customers_for_plot = customers
        ga_random_total_cost += ga_random_best_cost

    ga_random_total_cost /= UAV_V  # convert to time
    ga_random_total_cost += ga_rdb_truck_cost  # add truck time

    print("Total GA Random cost:", round(ga_random_total_cost, 2))
    plot_all_routes(
        customers=all_ga_random_customers_for_plot,
        stops=stops,
        results=ga_random_results,
        depot_route=ga_rdb_truck_depot_route,
        chrom=ga_best_solution,
        plotTitle="GA Clusters + Random Routes"
    )

    # Hybrid (ACO on GA clusters)
    hybrid_results = {}
    hybrid_total_cost = 0
    all_hybrid_customers_for_plot = []

    for stop_id, data in ga_clusters.items():

        stop = data["stop"]
        ga_cluster_customers = data["customers"]

        customers_for_hybrid = [stop] + ga_cluster_customers

        distance_matrix = build_distance_matrix_np(customers_for_hybrid)

        hybrid_aco = ACOOnly(
            customers=customers_for_hybrid,
            distance_matrix=distance_matrix,
            Qmax=Qmax,
            UAV_V=UAV_V
        )

        hybrid_best_routes, hybrid_best_cost = hybrid_aco.run()

        hybrid_results[stop_id] = {
            "stop": stop,
            "nodes": customers_for_hybrid,
            "routes": hybrid_best_routes,
            "cost": hybrid_best_cost
        }

        # store for global plotting
        all_hybrid_customers_for_plot = customers
        hybrid_total_cost += hybrid_best_cost

    hybrid_total_cost /= UAV_V  # convert to time
    hybrid_total_cost += hybrid_truck_cost  # add truck time

    print("Total Hybrid cost:", round(hybrid_total_cost, 2))
    plot_all_routes(
        customers=all_hybrid_customers_for_plot,
        stops=stops,
        results=hybrid_results,
        depot_route=hybrid_truck_depot_route,
        chrom=ga_best_solution,
        plotTitle="Hybrid GA + ACO: GA Clusters + ACO Routes"
    )

    plot_bar_comparison(
        costs=[round(trandom_total_cost, 2), round(random_aco_total_cost, 2), round(ga_random_total_cost, 2), round(hybrid_total_cost, 2)],
        labels=["True Random", "Random + ACO", "GA + Random", "Hybrid GA+ACO"],
        title="Total UAV Route Cost Comparison"
    )

# run all datasets
datasets = [
    ("Random Dataset 1", *generate_random_dataset(num_customers=200, num_stops=25, truckV=100, UAVV=50, seed = 42)),
    # ("Random Dataset 2", *generate_random_dataset(num_customers=200, num_stops=25, truckV=120, UAVV=50, seed = 2)),
    # ("Random Dataset 3", *generate_random_dataset(num_customers=200, num_stops=40, truckV=120, UAVV=50, seed = 3)),
    # ("Random Dataset 4", *generate_random_dataset(num_customers=200, num_stops=55, truckV=120, UAVV=50, seed = 4)),
]

for name, customers, stops, Qmax, truck_V, UAV_V in datasets:
    run_experiment(name, customers, stops, Qmax, truck_V, UAV_V)