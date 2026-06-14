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