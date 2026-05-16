from dataset import (
    generate_data,
    create_distance_matrix
)

from random_baseline import RandomRouting

from aco import AntColonyOptimizer

from visualization import (
    plot_routes,
    plot_convergence
)

# =========================================
# CONFIGURATION
# =========================================

NUM_CUSTOMERS = 10
VEHICLE_CAPACITY = 15

# =========================================
# DATASET
# =========================================

locations, demands = generate_data(
    NUM_CUSTOMERS
)

distance_matrix = create_distance_matrix(
    locations
)

# =========================================
# PRINT INPUT DATA
# =========================================

print("\n===== INPUT DATA =====")

print(f"\nVehicle Capacity: {VEHICLE_CAPACITY}")

print("\nCustomer Locations and Demands:")

for i in range(len(locations)):

    x = locations[i][0]
    y = locations[i][1]

    demand = demands[i]

    print(
        f"Node {i}: "
        f"({x:.2f}, {y:.2f}) "
        f"| Demand: {demand}"
    )

total_demand = sum(demands)

print(f"\nTotal Customer Demand: {total_demand}")

# =========================================
# RANDOM BASELINE
# =========================================

random_solver = RandomRouting(
    num_customers=NUM_CUSTOMERS,
    vehicle_capacity=VEHICLE_CAPACITY,
    distance_matrix=distance_matrix,
    demands=demands
)

random_routes, random_distance = (
    random_solver.run()
)

print("\n===== RANDOM BASELINE =====")

for idx, route in enumerate(random_routes):

    clean_route = [int(x) for x in route]

    print(
        f"Vehicle {idx+1}: "
        f"{clean_route}"
    )

print(
    f"\nRandom Total Distance: "
    f"{random_distance:.2f}\n"
)

# =========================================
# ACO OPTIMIZER
# =========================================

aco = AntColonyOptimizer(
    num_customers=NUM_CUSTOMERS,
    vehicle_capacity=VEHICLE_CAPACITY,
    distance_matrix=distance_matrix,
    demands=demands
)

best_routes, best_distance, distance_history = (
    aco.optimize()
)

# =========================================
# RESULTS
# =========================================

print("\n===== ACO BEST ROUTES =====")

for idx, route in enumerate(best_routes):

    clean_route = [int(x) for x in route]
    print(f"Vehicle {idx+1}: {clean_route}")
    

print(
    f"\nBest Total Distance: "
    f"{best_distance:.2f}\n"
)

# =========================================
# VISUALIZATION
# =========================================

plot_routes(
    best_routes,
    locations
)

plot_convergence(
    distance_history
)