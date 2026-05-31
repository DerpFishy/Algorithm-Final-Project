import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

# =========================
# 1. Convergence graph
# =========================
def plot_convergence(history):
    plt.figure()
    plt.plot(history)
    plt.title("GA Convergence Curve")
    plt.xlabel("Generation")
    plt.ylabel("Best Fitness")
    plt.show()


# =========================
# 2. Boxplot comparison
# =========================
def plot_boxplot(ga_scores, rand_scores):
    plt.figure()
    plt.boxplot([ga_scores, rand_scores], labels=["GA", "Random"])
    plt.title("GA vs Random Distribution")
    plt.ylabel("Cost")
    plt.show()


# =========================
# 3. Bar chart mean comparison
# =========================
def plot_bar(ga_scores, rand_scores):
    plt.figure()
    plt.bar(["GA", "Random"], [np.mean(ga_scores), np.mean(rand_scores)])
    plt.title("Average Performance Comparison")
    plt.ylabel("Cost")
    plt.show()


# =========================
# 4. Statistical test (t-test)
# =========================
def run_ttest(ga_scores, rand_scores):
    t_stat, p_value = stats.ttest_ind(ga_scores, rand_scores)
    print("\n===== T-TEST =====")
    print("t-statistic:", t_stat)
    print("p-value:", p_value)