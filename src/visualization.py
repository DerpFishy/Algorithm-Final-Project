import matplotlib.pyplot as plt

def plot_solution(ax, customers, stops, chrom, title):
    stop_order, assignment = chrom

    # customers
    for c in customers:
        ax.scatter(c["x"], c["y"], c="blue")
        ax.text(c["x"], c["y"], str(c["id"]), fontsize=8)

    # stops
    for s in stops:
        ax.scatter(s["x"], s["y"], c="red", marker="s")
        ax.text(s["x"], s["y"], f"S{s['id']}", fontsize=10)

    # assignment lines (customer → stop)
    for c, g in zip(customers, assignment):
        s = stops[g]
        ax.plot([c["x"], s["x"]], [c["y"], s["y"]], "gray", alpha=0.3)

    # truck route
    for i in range(len(stop_order) - 1):
        a = stops[stop_order[i]]
        b = stops[stop_order[i + 1]]
        ax.plot([a["x"], b["x"]], [a["y"], b["y"]], "red")

    ax.set_title(title)


def plot_side_by_side(customers, stops, ga_sol, rand_sol):
    fig, axs = plt.subplots(1, 2, figsize=(12, 5))

    plot_solution(axs[0], customers, stops, ga_sol, "GA Solution")
    plot_solution(axs[1], customers, stops, rand_sol, "Random Baseline")

    plt.tight_layout()
    plt.show()

def plot_bar_comparison(ga_score, rand_score):
    import matplotlib.pyplot as plt

    plt.figure()
    plt.bar(["GA", "Random"], [ga_score, rand_score])
    plt.title("Optimization Performance Comparison")
    plt.ylabel("Total Cost (Lower is Better)")
    plt.show()