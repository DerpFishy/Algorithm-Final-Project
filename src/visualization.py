import matplotlib.pyplot as plt

def plot_routes(routes,
                locations):

    plt.figure(figsize=(8, 6))

    for route in routes:

        coords = locations[route]

        plt.plot(
            coords[:, 0],
            coords[:, 1],
            marker='o'
        )

    # Depot
    plt.scatter(
        locations[0][0],
        locations[0][1],
        s=200,
        marker='s',
        label='Depot'
    )

    plt.title("ACO Delivery Routes")

    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")

    plt.legend()
    plt.grid(True)

    plt.show()


def plot_convergence(distance_history):

    plt.figure(figsize=(8, 5))

    plt.plot(distance_history)

    plt.title("ACO Convergence")

    plt.xlabel("Iteration")
    plt.ylabel("Best Distance")

    plt.grid(True)

    plt.show()

def plot_comparison(random_cost,
                    greedy_cost,
                    aco_cost):

    algorithms = [
        "Random",
        "Greedy",
        "ACO"
    ]

    costs = [
        random_cost,
        greedy_cost,
        aco_cost
    ]

    plt.figure(figsize=(8, 5))

    plt.bar(algorithms, costs)

    plt.title("CVRP Route Optimization Comparison")
    plt.ylabel("Total Distance")

    for i, cost in enumerate(costs):

        plt.text(
            i,
            cost,
            f"{cost:.2f}",
            ha='center',
            va='bottom'
        )

    plt.grid(axis='y', linestyle='--', alpha=0.5)

    plt.show()