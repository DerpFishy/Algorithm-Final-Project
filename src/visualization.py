import matplotlib.pyplot as plt

def plot_convergence(best_history):
    plt.figure(figsize=(8,5))

    plt.plot(best_history, linewidth=2)

    plt.title("GA Convergence Curve")
    plt.xlabel("Generation")
    plt.ylabel("Best Cost")

    plt.grid(True)
    plt.show()

def plot_solution(customers, stops, open_stops, assignments):

    plt.figure(figsize=(8, 6))

    # Candidate stops (gray)
    for i, s in enumerate(stops):
        plt.scatter(
            s["x"], s["y"],
            c="gray",
            marker="s",
            s=80,
            label="Candidate Stop" if i == 0 else ""
        )

    # Open stops (red)
    for i, s in enumerate(open_stops):
        plt.scatter(
            s["x"], s["y"],
            c="red",
            marker="s",
            s=160,
            label="Open Stop" if i == 0 else ""
        )

    # Customers (blue)
    for i, c in enumerate(customers):
        plt.scatter(
            c["x"], c["y"],
            c="blue",
            s=40,
            label="Customer" if i == 0 else ""
        )

    # Assignment lines
    for c, s in assignments:
        plt.plot(
            [c["x"], s["x"]],
            [c["y"], s["y"]],
            c="green",
            alpha=0.4
        )

    # Layout improvements
    plt.title("GA Stop Selection + Greedy Assignment")
    plt.legend()
    plt.grid(True)
    plt.axis("equal")

    plt.show()

def plot_solution_compare(customers, stops,
                          ga_open, ga_assign,
                          rb_open, rb_assign):

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # LEFT: GA
    ax = axes[0]
    ax.set_title("GA Solution")

    for i, s in enumerate(stops):
        ax.scatter(s["x"], s["y"], c="gray", marker="s", s=80,
                   label="Stop" if i == 0 else "")

    for s in ga_open:
        ax.scatter(s["x"], s["y"], c="red", marker="s", s=160)

    for c in customers:
        ax.scatter(c["x"], c["y"], c="blue", s=40)

    for c, s in ga_assign:
        ax.plot([c["x"], s["x"]], [c["y"], s["y"]], c="green", alpha=0.4)

    ax.grid(True)
    ax.axis("equal")

    # RIGHT: RANDOM
    ax = axes[1]
    ax.set_title("Random Baseline")

    for i, s in enumerate(stops):
        ax.scatter(s["x"], s["y"], c="gray", marker="s", s=80)

    for s in rb_open:
        ax.scatter(s["x"], s["y"], c="red", marker="s", s=160)

    for c in customers:
        ax.scatter(c["x"], c["y"], c="blue", s=40)

    for c, s in rb_assign:
        ax.plot([c["x"], s["x"]], [c["y"], s["y"]], c="green", alpha=0.4)

    ax.grid(True)
    ax.axis("equal")

    plt.tight_layout()
    plt.show()

def plot_all_aco_routes(customers, stops, aco_results, depot_route, chrom):

    plt.figure(figsize=(12, 8))

    # CUSTOMERS
    for c in customers:
        plt.scatter(c["x"], c["y"], c="blue", s=40)

        plt.text(
            c["x"], c["y"],
            f"{c.get('q', 0)}",
            fontsize=7,
            ha="center",
            va="bottom",
            bbox=dict(facecolor="white", alpha=0.6, edgecolor="none")
        )

    # DEPOTS / STOPS
    used_x, used_y = [], []
    unused_x, unused_y = [], []

    for i, s in enumerate(stops):
        if chrom[i] == 1:
            used_x.append(s["x"])
            used_y.append(s["y"])
        else:
            unused_x.append(s["x"])
            unused_y.append(s["y"])

    plt.scatter(unused_x, unused_y, c="lightgray", marker="s", s=100, alpha=0.5, label="Unused Depot")
    plt.scatter(used_x, used_y, c="green", marker="s", s=140, label="Used Depot")

    # UAV ROUTES (ACO)
    colors = ["orange", "green", "purple", "brown", "pink", "cyan"]

    for i, (stop_id, data) in enumerate(aco_results.items()):

        color = colors[i % len(colors)]
        node_list = data["nodes"]

        for route in data["routes"]:

            xs = []
            ys = []

            for idx in route:
                node = node_list[idx]
                xs.append(node["x"])
                ys.append(node["y"])

            plt.plot(xs, ys, color=color, linewidth=.5, alpha=0.8)

            for j in range(len(xs) - 1):
                plt.annotate(
                    "",
                    xy=(xs[j+1], ys[j+1]),
                    xytext=(xs[j], ys[j]),
                    arrowprops=dict(
                        arrowstyle="->",
                        color=color,
                        alpha=0.7,
                        lw=.5
                    )
                )

    # DEPOT (TRUCK) ROUTE
    if depot_route is not None:

        dx = []
        dy = []

        used_depots = [s for i, s in enumerate(stops) if chrom[i] == 1]

        for depot_idx in depot_route:
            depot = used_depots[depot_idx]
            dx.append(depot["x"])
            dy.append(depot["y"])

        # draw truck path (thick dashed line)
        plt.plot(
            dx,
            dy,
            color="black",
            linestyle="--",
            linewidth=1,
            label="Truck Route (Depot Path)"
        )

        # arrows for truck route
        for i in range(len(dx) - 1):
            plt.annotate(
                "",
                xy=(dx[i+1], dy[i+1]),
                xytext=(dx[i], dy[i]),
                arrowprops=dict(
                    arrowstyle="->",
                    color="black",
                    lw=1,
                    alpha=0.9
                )
            )

        # highlight start/end depot
        plt.scatter(dx[0], dy[0], c="black", s=10, marker="*", label="Start Depot")

    # FINAL STYLE
    plt.title("Hybrid GA + ACO: Truck Depot Routing + UAV Routing")
    plt.grid(True)
    plt.axis("equal")
    plt.legend()
    plt.show()