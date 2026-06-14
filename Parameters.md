# 1. GAOnly (Genetic Algorithm) Parameters

Based on your configuration code, the genetic algorithm uses a blend of static thresholds and dynamically scaled variables:

* **Population Size ($N$):** Scales dynamically based on the total number of stops, bounded between $30$ and $500$.
  $$N = \max\left(30, \min\left(500, 10 \cdot |S|\right)\right)$$
* **Elite Size ($N_e$):** Retains the top $10\%$ of the population, with a minimum of 2 individuals.
  $$N_e = \max\left(2, \lfloor N / 10 \rfloor\right)$$
* **Tournament Size ($k$):** $5$ candidate chromosomes are sampled per round.
* **Crossover Probability ($p_c$):** $0.5$ ($50\%$ uniform swap chance per gene bit).
* **Mutation Rate ($r_m$):** $0.3$ ($30\%$ bitwise inversion probability per gene).
* **Diversity Injection Probability:** $0.1$ ($10\%$ chance to replace an individual just past the elite threshold with a random chromosome).

### Evaluator-Specific Objective Coefficients
* **Maximum Distance Threshold ($D_{\max}$):** $1$
* **Distance Penalty Multiplier:** $10$ (applied linearly to any distance violating $D_{\max}$).
* **Facility Scale Weight ($\alpha$):** $1$
* **Unused Facility Open Penalty Weight:** $5.0$

---

# 2. DepotACO (Ant Colony Optimization) Parameters

The standard Traveling Salesperson version of your ant system utilizes the following configurations:

* **Ant Count ($m$):** $10$ ants per iteration.
* **Pheromone Sensitivity ($\alpha$):** $1.5$
* **Distance Heuristic Sensitivity ($\beta$):** $1.5$
* **Evaporation / Decay Rate ($\rho$):** $0.2$ ($20\%$ loss per iteration).
* **Pheromone Lower-Bound Offset ($\epsilon$):** $10^{-9}$ (prevents division-by-zero errors during visibility calculations and pheromone scaling).

---

# 3. ACOOnly (UAV Capacitated ACO) Parameters

The multi-route vehicle variant maps out solutions using these constraints and variables:

* **Ant Count ($m$):** $10$ ants per iteration.
* **Pheromone Sensitivity ($\alpha$):** $1.5$
* **Distance Heuristic Sensitivity ($\beta$):** $1.5$
* **Evaporation / Decay Rate ($\rho$):** $0.2$
* **Stochastic Exploration Rate ($\epsilon$):** $0.1$ ($10\%$ chance to skip pheromone rules and pick a feasible node completely at random).
* **Elitist Selection Proportion ($K$):** Top $20\%$ of ants deposit pheromones.
  $$K = \max\left(1, \lfloor m / 5 \rfloor\right)$$