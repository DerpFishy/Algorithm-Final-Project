from ga_only import GAOnly
from random_selection_baseline import RandomSelectionBaseline
from random_depot_baseline import RandomDepotBaseline
from random_uav_baseline import RandomUAVBaseline
from aco_only import ACOOnly
from depot_aco import DepotACO
from helper import build_clusters, build_distance_matrix_np, build_customer_stop_matrix
from data.dataset import generate_random_dataset
from visualization import plot_convergence, plot_dataset, plot_ga_solution, plot_solution_compare, plot_bar_compare, plot_all_routes, plot_bar_comparison
from statistic import assignment_mean, statistical_analysis

def run_experiment(name, customers, stops, Qmax, truck_V, UAV_V, visualize=True):
    print("\n======================")
    print("Dataset:", name)
    print("======================")

    customer_stop_matrix = build_customer_stop_matrix(customers, stops)

    if visualize:
        plot_dataset(customers=customers, stops=stops)

    rsb = RandomSelectionBaseline(customers, stops, customer_stop_matrix)

    rsb_solution, rsb_cost, rsb_open, rsb_assign, rsb_hist = rsb.run(min(100000, 15 * len(customers) * len(stops)))
    rsb_cost = round(rsb_cost, 2)
    if visualize:
        print("RSB solution:", rsb_solution)
        print("RSB cost:", rsb_cost)

    ga = GAOnly(customers, stops, customer_stop_matrix)
    ga_best_solution, ga_best_cost, ga_open_stops, ga_assignments, ga_best_history = ga.run(min(400, 15 * len(stops)))
    ga_best_cost = round(ga_best_cost, 2)

    # VISUALIZATION
    if visualize:
        print("Best solution:", ga_best_solution)
        print("Best cost:", ga_best_cost)
    if visualize:
        plot_convergence(ga_best_history)
        plot_bar_compare(
            name1="RSB",
            value1=rsb_cost,
            name2="GA",
            value2=ga_best_cost,
            nameY="Assignment Cost",
            title="RSB vs GA")
        plot_ga_solution(
            customers=customers,
            stops=stops,
            ga_open=ga_open_stops,
            ga_assign=ga_assignments
        )
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
    if visualize:
        print("TRDB Truck route:", trdb_truck_depot_route)
        print("TRDB Truck route cost:", round(trdb_truck_cost, 2))

    random_aco = DepotACO(rsb_open, rsb_depot_matrix, truck_V)
    random_aco_truck_depot_route, random_aco_truck_cost = random_aco.run()
    random_aco_truck_cost /= truck_V  # convert to time
    if visualize:
        print("Random ACO Truck route:", random_aco_truck_depot_route)
        print("Random ACO Truck route cost:", round(random_aco_truck_cost, 2))

    ga_rdb = RandomDepotBaseline(ga_depots, ga_depot_matrix, truck_V)
    ga_rdb_truck_depot_route, ga_rdb_truck_cost = ga_rdb.run((len(ga_depots) ** 2) * 10)
    ga_rdb_truck_cost /= truck_V  # convert to time
    if visualize:
        print("GA RDB Truck route:", ga_rdb_truck_depot_route)
        print("GA RDB Truck route cost:", round(ga_rdb_truck_cost, 2))

    hybrid_truck = DepotACO(ga_depots, ga_depot_matrix, truck_V)
    hybrid_truck_depot_route, hybrid_truck_cost = hybrid_truck.run()
    hybrid_truck_cost /= truck_V  # convert to time
    if visualize:
        print("Hybrid Truck route:", hybrid_truck_depot_route)
        print("Hybrid Truck route cost:", round(hybrid_truck_cost, 2))

    if visualize:
        plot_bar_comparison(
            costs=[round(trdb_truck_cost, 2), round(random_aco_truck_cost, 2), round(ga_rdb_truck_cost, 2), round(hybrid_truck_cost, 2)],
            labels=["True Random", "Random + ACO", "GA + Random", "Hybrid GA+ACO"],
            title="Total Truck Route Cost Comparison"
        )

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

    if visualize:
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

    if visualize:
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

    if visualize:
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

    if visualize:
        print("Total Hybrid cost:", round(hybrid_total_cost, 2))
        plot_all_routes(
            customers=all_hybrid_customers_for_plot,
            stops=stops,
            results=hybrid_results,
            depot_route=hybrid_truck_depot_route,
            chrom=ga_best_solution,
            plotTitle="Hybrid GA + ACO: GA Clusters + ACO Routes"
        )

    if visualize:
        plot_bar_comparison(
            costs=[round(trandom_total_cost, 2), round(random_aco_total_cost, 2), round(ga_random_total_cost, 2), round(hybrid_total_cost, 2)],
            labels=["True Random", "Random + ACO", "GA + Random", "Hybrid GA+ACO"],
            title="Total Time Comparison"
        )
    
    return {
        "dataset": name,
        "rsb_cost": rsb_cost,
        "ga_cost": ga_best_cost,
        "true_random": trandom_total_cost,
        "random_aco": random_aco_total_cost,
        "ga_random": ga_random_total_cost,
        "hybrid": hybrid_total_cost
    }

def benchmark(datasets):
    results = []

    for name, customers, stops, Qmax, truck_V, UAV_V in datasets:
        result = run_experiment(name, customers, stops, Qmax, truck_V, UAV_V, visualize=False)
        results.append(result)

    assignment_mean(results)
    statistical_analysis(results)

datasets = []

# # run test datasets
# datasets = [
#     ("Test Dataset", *generate_random_dataset(num_customers=200, num_stops=25, truckV=100, UAVV=50, seed = 42))
# ]

# # correctness test dataset
# datasets = [
# # =========================
# # Dataset 1: Cluster + Scatter Mix
# # =========================
# ("Dataset 1: Mixed Clusters",
#  [
#      {"id": 0, "x": 1.2, "y": 2.8, "q": 3},
#      {"id": 1, "x": 2.0, "y": 1.5, "q": 4},
#      {"id": 2, "x": 2.8, "y": 3.2, "q": 2},
#      {"id": 3, "x": 4.5, "y": 4.0, "q": 5},
#      {"id": 4, "x": 5.2, "y": 5.8, "q": 3},

#      {"id": 5, "x": 10.5, "y": 2.2, "q": 4},
#      {"id": 6, "x": 11.8, "y": 3.5, "q": 2},
#      {"id": 7, "x": 12.2, "y": 1.8, "q": 3},

#      {"id": 8, "x": 7.0, "y": 9.5, "q": 4},
#      {"id": 9, "x": 8.5, "y": 10.2, "q": 2},
#  ],
#  [
#      {"id": 0, "x": 2.0, "y": 2.0},
#      {"id": 1, "x": 11.0, "y": 2.5},
#      {"id": 2, "x": 8.0, "y": 9.5},
#  ],
#  15, 100, 50),
# # =========================
# # Dataset 2: Circular / Radial Spread (no linear patterns)
# # =========================
# ("Dataset 2: Radial Spread",
#  [
#      {"id": 0, "x": 7.5, "y": 2.0, "q": 3},
#      {"id": 1, "x": 10.5, "y": 3.5, "q": 4},
#      {"id": 2, "x": 12.0, "y": 7.5, "q": 2},
#      {"id": 3, "x": 10.0, "y": 11.0, "q": 3},
#      {"id": 4, "x": 7.5, "y": 13.0, "q": 5},

#      {"id": 5, "x": 4.0, "y": 11.5, "q": 2},
#      {"id": 6, "x": 3.0, "y": 7.0, "q": 3},
#      {"id": 7, "x": 4.5, "y": 3.5, "q": 4},

#      {"id": 8, "x": 6.0, "y": 6.0, "q": 2},
#      {"id": 9, "x": 9.0, "y": 9.0, "q": 3},
#  ],
#  [
#      {"id": 0, "x": 7.5, "y": 7.5},
#      {"id": 1, "x": 2.5, "y": 2.5},
#      {"id": 2, "x": 12.5, "y": 12.5},
#  ],
#  15, 100, 50),
# # =========================
# # Dataset 3: Random Balanced (good stress test)
# # =========================
# ("Dataset 3: Random Balanced Field",
#  [
#      {"id": 0, "x": 1.5, "y": 12.5, "q": 2},
#      {"id": 1, "x": 2.8, "y": 9.2, "q": 4},
#      {"id": 2, "x": 3.5, "y": 5.5, "q": 3},
#      {"id": 3, "x": 5.0, "y": 2.5, "q": 5},
#      {"id": 4, "x": 6.5, "y": 10.5, "q": 2},

#      {"id": 5, "x": 8.0, "y": 8.0, "q": 3},
#      {"id": 6, "x": 9.5, "y": 6.5, "q": 4},
#      {"id": 7, "x": 11.0, "y": 3.0, "q": 2},
#      {"id": 8, "x": 12.5, "y": 11.5, "q": 3},
#      {"id": 9, "x": 13.5, "y": 7.5, "q": 2},
#  ],
#  [
#      {"id": 0, "x": 2.0, "y": 12.0},
#      {"id": 1, "x": 7.5, "y": 7.5},
#      {"id": 2, "x": 12.5, "y": 2.5},
#  ],
#  15, 100, 50),
# ]

for name, customers, stops, Qmax, truck_V, UAV_V in datasets:
    run_experiment(name, customers, stops, Qmax, truck_V, UAV_V, visualize=True)

# # run benchmark for stats for 30 runs
# datasets = []
# for i in range(30):
#     dataset = (f"Random Dataset {i}", *generate_random_dataset(num_customers=200, num_stops=25, truckV=100, UAVV=50, seed=i))
#     datasets.append(dataset)
# benchmark(datasets)