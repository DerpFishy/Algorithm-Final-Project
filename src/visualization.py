import matplotlib.pyplot as plt


def plot_solution(customers, stops, open_stops, assignments):

    plt.figure(figsize=(8, 6))

    # ---------------------------
    # Candidate stops (gray)
    # ---------------------------
    for i, s in enumerate(stops):
        plt.scatter(
            s["x"], s["y"],
            c="gray",
            marker="s",
            s=80,
            label="Candidate Stop" if i == 0 else ""
        )

    # ---------------------------
    # Open stops (red)
    # ---------------------------
    for i, s in enumerate(open_stops):
        plt.scatter(
            s["x"], s["y"],
            c="red",
            marker="s",
            s=160,
            label="Open Stop" if i == 0 else ""
        )

    # ---------------------------
    # Customers (blue)
    # ---------------------------
    for i, c in enumerate(customers):
        plt.scatter(
            c["x"], c["y"],
            c="blue",
            s=40,
            label="Customer" if i == 0 else ""
        )

    # ---------------------------
    # Assignment lines
    # ---------------------------
    for c, s in assignments:
        plt.plot(
            [c["x"], s["x"]],
            [c["y"], s["y"]],
            c="green",
            alpha=0.4
        )

    # ---------------------------
    # Layout improvements
    # ---------------------------
    plt.title("GA Stop Selection + Greedy Assignment")
    plt.legend()
    plt.grid(True)
    plt.axis("equal")

    plt.show()