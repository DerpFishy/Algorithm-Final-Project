import matplotlib.pyplot as plt
from scipy.stats import ttest_rel
import statistics

def assignment_mean(results):
    plt.figure(figsize=(6,4))

    plt.boxplot(
        [[res["rsb_cost"] for res in results], [res["ga_cost"] for res in results]],
        tick_labels=["RSB", "GA"]
    )

    plt.ylabel("Assignment Cost")
    plt.title("Average Assignment Cost")
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.show()

def statistical_analysis(results):

    true_random = [r["true_random"] for r in results]
    random_aco = [r["random_aco"] for r in results]
    ga_random = [r["ga_random"] for r in results]
    hybrid = [r["hybrid"] for r in results]

    print("\n======================")
    print("STATISTICAL ANALYSIS")
    print("======================")

    print(f"Mean True Random : {statistics.mean(true_random):.4f}")
    print(f"Mean Random ACO  : {statistics.mean(random_aco):.4f}")
    print(f"Mean GA Random   : {statistics.mean(ga_random):.4f}")
    print(f"Mean Hybrid      : {statistics.mean(hybrid):.4f}")

    comparisons = [
        ("Hybrid vs Random ACO", random_aco, hybrid),
        ("Hybrid vs GA Random", ga_random, hybrid),
        ("Hybrid vs True Random", true_random, hybrid)
    ]

    for title, baseline, hybrid_data in comparisons:

        t_stat, p_value = ttest_rel(baseline, hybrid_data)

        print(f"\n{title}")
        print(f"T-statistic = {t_stat:.4f}")
        print(f"P-value     = {p_value:.6f}")

        if p_value < 0.05:
            print("Result: Significant")
        else:
            print("Result: Not Significant")

    plt.figure(figsize=(8, 6))

    # Combine all 4 data streams into a list of lists
    data_to_plot = [
        [res["true_random"] for res in results],
        [res["ga_random"] for res in results],
        [res["random_aco"] for res in results],
        [res["hybrid"] for res in results]
    ]

    # Create the boxplot
    plt.boxplot(data_to_plot, tick_labels=["True Random", "GA Random", "Random ACO", "Hybrid"])

    # Add styling
    plt.title("Distribution of Total Costs Across 30 Runs", fontsize=14, fontweight='bold')
    plt.ylabel("Total Cost", fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.5)

    # Optional: Highlight your winning algorithm's background or box if you want to be fancy
    plt.show()