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