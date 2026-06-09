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