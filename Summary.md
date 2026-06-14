# Comprehensive Optimization Suite Summary

Your codebase establishes an algorithmic optimization suite designed to solve complex logistics, routing, and facility location challenges. It breaks down into three distinct problem domains, comparing specialized metaheuristics (**Genetic Algorithms** and **Ant Colony Optimization**) against stochastic **Random Baselines** to benchmark performance.

---

### 1. Stop Selection & Customer Assignment Domain
This domain solves a variant of the **Uncapacitated Facility Location Problem (UFLP)**. It balances the operational cost of keeping transit stops open against the convenience (distance) of the customers using them.

* **GAOnly (Genetic Algorithm Metaheuristic):** Uses an evolutionary approach ($N$ individuals). It utilizes **Tournament Selection** to pick the fittest parents, **Uniform Crossover** to blend configurations, and **Bit-Flip Mutation** (with a validity guard to ensure at least one stop stays open) to explore new structures. It features an **Elitism** mechanism and a **Diversity Injection** step to prevent population stagnation.
* **RandomSelectionBaseline:** Generates purely random binary configurations ($x_j \in \{0, 1\}$) over a set number of iterations to establish the absolute lower-bound performance expectation.
* **The Evaluator (Core Objective Function):** Both algorithms use this to minimize a combined cost function:
    $$\min f(\mathbf{x}) = \text{Average Customer Distance} + \text{Distance Penalty} + \alpha\sqrt{\text{Open Stops}} + \text{Unused Stop Penalty}$$

---

### 2. Depot Routing Domain
This domain handles standard routing optimization, modeled as a **Traveling Salesperson Problem (TSP)**, to discover the shortest cyclic path that visits every depot exactly once and returns to the origin.

* **DepotACO (Ant Colony Optimization System):** Simulates a colony of $10$ ants. Ants construct paths stochastically based on an edge score combining historical pheromone intensity ($\alpha=1.5$) and a distance-inverse heuristic ($\beta=1.5$). At each iteration's end, pheromones undergo global evaporation ($\rho=0.2$) and are reinforced by paths containing lower overall costs.
* **RandomDepotBaseline:** Shuffles the index array of remaining depots using a uniform pseudo-random number generator to build a valid cyclic permutation, acting as a baseline benchmark for the ACO.

---

### 3. UAV Payload Delivery Domain
This domain tackles the **Capacitated Vehicle Routing Problem (CVRP)**, optimizing a fleet of UAVs that must deliver goods from a central hub to multiple customers while respecting a maximum payload limit ($Q_{\max}$).

* **ACOOnly (Capacitated Ant Colony Metaheuristic):** Features a specialized state transition rule that filters out unvisited nodes violating the remaining capacity constraint ($q_j > Q_{\text{left}}$). It implements an **$\epsilon$-greedy strategy** ($10\%$ pure random exploration) to avoid local minima, and utilizes an **Elitist/Ranked Pheromone Update** where only the top $20\%$ highest-performing ants are allowed to deposit pheromones.
* **RandomUAVBaseline:** Constructs legal, capacity-compliant sub-routes by choosing uniformly at random from the pool of currently feasible customers. When a vehicle runs out of capacity, it dynamically resets at the depot and deploys another simulated UAV until all customer demands are satisfied.

---

### Parameter Reference Matrix

The following table compiles all configurations across your metaheuristic implementations:

| Algorithm / Module | Parameter | Variable / Rule | Value / Expression |
| :--- | :--- | :--- | :--- |
| **GAOnly** | Population Size | $N$ | $\max(30, \min(500, 10 \cdot \vert S \vert))$ |
| | Elite Size | $N_e$ | $\max(2, \lfloor N / 10 \rfloor)$ |
| | Mutation Rate / Crossover | $r_m \; / \; p_c$ | $0.3 \; / \; 0.5$ |
| **Evaluator** | Max Distance Threshold | $D_{\max}$ | $1$ |
| | Distance Violations / Unused Stop | Penalty Weights | $10.0 \; / \; 5.0$ |
| **DepotACO** | Ant Count / Evaporation | $m \; / \; \rho$ | $10 \; / \; 0.2$ |
| | Pheromone / Heuristic | $\alpha \; / \; \beta$ | $1.5 \; / \; 1.5$ |
| **ACOOnly** | Fleet Exploration Rate | $\epsilon$ | $0.1$ |
| | Pheromone Update Strategy | Elitist Rank ($K$) | $\max(1, \lfloor m / 5 \rfloor)$ (Top $20\%$) |

# Summary of Statistical Analysis

The statistical analysis evaluates the performance of four algorithmic configurations based on their mean cost scores: **True Random**, **GA Random**, **Random ACO**, and your proposed **Hybrid** algorithm. Lower mean scores indicate better, more optimized solutions.

### 1. Performance Ranking (Mean Costs)
The algorithms rank from best (lowest cost) to worst (highest cost) as follows:

1. **Hybrid:** **5.0094** *(Top Performer)*
2. **Random ACO:** **5.1094**
3. **Mean GA Random:** **6.2798**
4. **True Random:** **6.4219** *(Baseline)*

---

### 2. Hypothesis Testing & Significance
To determine if the Hybrid algorithm's superior performance is mathematically meaningful or just due to lucky sampling, a series of t-tests were conducted against the other three configurations. 

* **Hybrid vs. True Random ($p = 0.000000$):** **Highly Significant.** The Hybrid algorithm drastically outperforms blind random searching ($t = 38.62$), confirming its optimization mechanics are working exceptionally well.
* **Hybrid vs. GA Random ($p = 0.000000$):** **Highly Significant.** With an massive t-statistic of $45.01$, the Hybrid algorithm demonstrates a monumental performance leap over using a Genetic Algorithm approach on its own.
* **Hybrid vs. Random ACO ($p = 0.000014$):** **Statistically Significant.** While Random ACO is quite competitive (only $0.1$ higher on average), the t-test confirms that the Hybrid algorithm still achieves a genuinely superior edge ($t = 5.22$). The incredibly low p-value rules out random chance.

---

### 3. Key Takeaway
The **Hybrid algorithm is the definitive winner**. It successfully leverages the strengths of both metaheuristics to outperform the individual standalone baselines and random searches with absolute statistical certainty.