import matplotlib.pyplot as plt

def plot_convergence(best_history):
    plt.figure(figsize=(8,5))

    plt.plot(best_history, linewidth=2)

    plt.title("GA Convergence Curve")
    plt.xlabel("Generation")
    plt.ylabel("Best Cost")

    plt.grid(True)
    plt.show()

def plot_bar_compare(name1, value1, name2, value2, nameY, title):
    bars = plt.bar(
        [name1, name2],
        [value1, value2],
        color=['#3498db', '#e74c3c']
    )

    plt.ylabel(nameY)
    plt.title(title)

    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width()/2,
            height,
            f"{height:.2f}",
            ha="center",
            va="bottom"
        )

    plt.show()

def plot_dataset(customers, stops):
    plt.figure(figsize=(7, 6))
    ax = plt.gca()

    ax.set_title("Dataset")

    # All stops
    for i, s in enumerate(stops):
        ax.scatter(s["x"], s["y"], c="gray", marker="s", s=160,
                   label="Stop" if i == 0 else "")

    # All Customers
    for i, c in enumerate(customers):
        ax.scatter(c["x"], c["y"], c="blue", s=40,
                   label="Customer" if i == 0 else "")

    ax.grid(True)
    ax.axis("equal")
    ax.legend()

    plt.tight_layout()
    plt.show()

def plot_ga_solution(customers, stops, ga_open, ga_assign):
    plt.figure(figsize=(7, 6))
    ax = plt.gca()

    ax.set_title("GA Solution")

    # All stops (background)
    for i, s in enumerate(stops):
        ax.scatter(s["x"], s["y"], c="gray", marker="s", s=80,
                   label="Stop" if i == 0 else "")

    # Open GA-selected stops
    for i, s in enumerate(ga_open):
        ax.scatter(s["x"], s["y"], c="red", marker="s", s=160,
                   label="Open Stop" if i == 0 else "")

    # Customers
    for i, c in enumerate(customers):
        ax.scatter(c["x"], c["y"], c="blue", s=40,
                   label="Customer" if i == 0 else "")

    # Assignments (edges)
    for c, s in ga_assign:
        ax.plot([c["x"], s["x"]], [c["y"], s["y"]],
                c="green", alpha=0.4)

    ax.grid(True)
    ax.axis("equal")
    ax.legend()

    plt.tight_layout()
    plt.show()

def plot_solution_compare(customers, stops,
                          ga_open, ga_assign,
                          rsb_open, rsb_assign):

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # LEFT: RANDOM
    ax = axes[0]
    ax.set_title("Random Selection Baseline")

    for i, s in enumerate(stops):
        ax.scatter(s["x"], s["y"], c="gray", marker="s", s=80)

    for s in rsb_open:
        ax.scatter(s["x"], s["y"], c="red", marker="s", s=160)

    for c in customers:
        ax.scatter(c["x"], c["y"], c="blue", s=40)

    for c, s in rsb_assign:
        ax.plot([c["x"], s["x"]], [c["y"], s["y"]], c="green", alpha=0.4)

    ax.grid(True)
    ax.axis("equal")

    # RIGHT: GA
    ax = axes[1]
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

    plt.tight_layout()
    plt.show()

def plot_all_routes(customers, stops, results, depot_route, chrom, plotTitle):

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

    for i, (stop_id, data) in enumerate(results.items()):

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
    plt.title(plotTitle)
    plt.grid(True)
    plt.axis("equal")
    plt.legend()
    plt.show()

def plot_bar_comparison(costs, labels=None, title="Result Comparison"):
    if len(costs) != 4:
        print("Error: Please provide exactly 4 values.")
        return

    # If no labels are provided, use default A, B, C, D
    if labels is None:
        labels = ['Value 1', 'Value 2', 'Value 3', 'Value 4']

    # Create the plot
    plt.figure(figsize=(8, 5))
    bars = plt.bar(labels, costs, color=['#3498db', '#e74c3c', '#2ecc71', '#f1c40f'])

    # Add details
    plt.title(title, fontsize=14)
    plt.ylabel('Costs')
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Add value labels on top of each bar
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + .05, yval, ha='center', va='bottom')

    # Show the plot
    plt.show()