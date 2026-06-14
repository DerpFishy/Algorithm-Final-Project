# 1. RandomSelectionBaseline: Mathematical Formulation

The `RandomSelectionBaseline` serves as a random search baseline for the facility location problem. It samples entirely random configurations across the solution space over a fixed number of iterations.

### A. Core Search Space
Let $\mathbf{x} = [x_1, x_2, \dots, x_{|S|}]$ be a binary vector representing the activation state of each stop. In each iteration $k \in \{1, \dots, \text{iterations}\}$, each gene $x_j$ is generated via independent discrete uniform sampling:

$$x_j^{(k)} \sim \mathcal{U}_{\text{discrete}}(0, 1) \quad \forall j \in S$$

### B. Objective Selection
The algorithm evaluates each random vector using the exact same fitness function $f(\mathbf{x})$ defined in your `Evaluator` class:

$$\min_{\mathbf{x}} \quad f(\mathbf{x}) = T(\mathbf{x}) + F(\mathbf{x}) + P(\mathbf{x})$$

The baseline keeps track of the global minimum across all sampled solutions:

$$\mathbf{x}_{\text{best}} = \arg\min_{k} f\left(\mathbf{x}^{(k)}\right)$$

---

# 2. RandomDepotBaseline: Mathematical Formulation

The `RandomDepotBaseline` provides a pure random permutation approach to solve a basic Traveling Salesperson Problem (TSP) over a network of depots.

### A. Permutation Generation
Let $S = \{0, 1, \dots, n-1\}$ be the set of depot indices. For each trial $t \in \{1, \dots, \text{trials}\}$:
1. A starting depot $d_{\text{start}}$ is sampled uniformly: 
   $$d_{\text{start}} \sim \mathcal{U}_{\text{discrete}}(0, n-1)$$
2. A random permutation $\sigma$ is created from the remaining depots $S \setminus \{d_{\text{start}}\}$. Let this shuffled sequence be $[r_1, r_2, \dots, r_{n-1}]$.

The complete cyclic route vector $\mathbf{R}^{(t)}$ is formulated as:

$$\mathbf{R}^{(t)} = [d_{\text{start}}, r_1, r_2, \dots, r_{n-1}, d_{\text{start}}]$$

### B. Cost Minimization
The objective is to minimize total round-trip distance. The cost $C\left(\mathbf{R}^{(t)}\right)$ is calculated as:

$$C\left(\mathbf{R}^{(t)}\right) = \sum_{i=0}^{n-1} d_{\mathbf{R}_i^{(t)}, \, \mathbf{R}_{i+1}^{(t)}}$$

Where $d_{ij}$ is the distance matrix element between depot $i$ and $j$. The best route retains:

$$\mathbf{R}_{\text{best}} = \arg\min_{t} C\left(\mathbf{R}^{(t)}\right)$$

---

# 3. RandomUAVBaseline: Mathematical Formulation

The `RandomUAVBaseline` provides a randomized heuristic solution for the Capacitated Vehicle Routing Problem (CVRP) with payload constraints.

### A. Randomized Feasible Sub-Route Construction
Let $\{0\}$ be the central depot, and $C = \{1, 2, \dots, n-1\}$ be the set of unvisited customers. At any point during a trial, if a vehicle is at node $i$ with a remaining cargo capacity $Q_{\text{left}}$, its candidate node pool is restricted to the feasible set $\mathcal{F}(Q_{\text{left}})$:

$$\mathcal{F}(Q_{\text{left}}) = \{ j \in \text{unvisited} \mid q_j \le Q_{\text{left}} \}$$

Instead of evaluating pheromones or heuristics, the next destination $nxt$ is selected via a uniform random choice over the feasible set:

$$nxt \sim \mathcal{U}_{\text{discrete}}\left(\mathcal{F}(Q_{\text{left}})\right)$$

When $\mathcal{F}(Q_{\text{left}}) = \emptyset$, the vehicle returns to the depot $\{0\}$, resetting its capacity back to $Q_{\max}$ to build the next sub-route until $\text{unvisited} = \emptyset$.

### B. Fleet Cost Optimization
For a complete generated fleet solution $\mathbf{M}^{(t)} = \{\text{route}_1, \text{route}_2, \dots, \text{route}_m\}$ in trial $t$, the total fitness is the sum of lengths across all independent UAV routes:

$$C\left(\mathbf{M}^{(t)}\right) = \sum_{\mathbf{r} \in \mathbf{M}^{(t)}} \sum_{i=0}^{|\mathbf{r}|-2} d_{\mathbf{r}_i, \, \mathbf{r}_{i+1}}$$

The baseline tracks the overall lowest energy/distance cost configuration:

$$\mathbf{M}_{\text{best}} = \arg\min_{t} C\left(\mathbf{M}^{(t)}\right)$$

# Summary of Random Baselines

The random baseline modules in your codebase establish a control group for your optimization suite. By stripped-down, purely stochastic search methods, they define the baseline performance (the "floor") of your system. This allows you to measure exactly how much value your metaheuristics (**Genetic Algorithms** and **Ant Colony Optimization**) actually add.

---

### 1. RandomSelectionBaseline (Facility Location)
This baseline targets the **Stop Selection & Customer Assignment** problem. Instead of using evolutionary pressure to find out which transit stops to open, it relies entirely on blind luck.

* **How it works:** In each iteration, it rolls a virtual fair coin for every single stop to decide whether it should be open ($1$) or closed ($0$). 
* **Evaluation:** It passes this random combination to the exact same `Evaluator` class used by the Genetic Algorithm, calculates the score, and saves the configuration if it happens to beat the previous best random attempt.
* **Purpose:** It proves whether the GA's selection and crossover mechanics are actively finding smart facility clusters, or if random guessing could achieve a similar cost.

---

### 2. RandomDepotBaseline (Traveling Salesperson Problem)
This module acts as the control group for the **Depot Routing** domain, where the goal is to find the shortest loop connecting all depots.

* **How it works:** It randomly picks an anchor depot to start at. Then, it takes all the remaining depots and uses a pseudo-random shuffle to scramble their order. Finally, it tacks the starting depot onto the end to close the loop.
* **Evaluation:** It measures the total distance of this random permutation over a series of independent trials (defaulting to $1,000$) and tracks the shortest route found.
* **Purpose:** It benchmarks the `DepotACO` algorithm. If the Ant Colony Optimization can't significantly beat this baseline, it indicates that the pheromone sensitivity ($\alpha$) or heuristic weight ($\beta$) needs tuning.

---

### 3. RandomUAVBaseline (Capacitated Vehicle Routing)
This baseline handles the **UAV Payload Delivery** problem, where multiple delivery routes must be drawn without overloading any single drone's cargo capacity ($Q_{\max}$).

* **How it works:** It builds valid routes sequentially. A simulated drone starts at the hub and looks at all unvisited customers whose package weight fits within its remaining payload. Instead of using pheromone trails or distance heuristics to choose the next stop, it picks one completely at random. 
* **Dynamic Reset:** Once the drone is too full to accept any more nearby packages, it "returns" to the hub. Its capacity resets, and a new route begins. This loop repeats until every customer is assigned to a route.
* **Purpose:** It establishes the baseline fleet cost for the `ACOOnly` class. It isolates whether the elitist ranking and pheromone evaporation strategies are successfully minimizing flight energy, or if simply keeping routes capacity-compliant is enough.

---

### Core Comparison Matrix

| Baseline Class | Target Problem Domain | Search Strategy | Constraint Handling |
| :--- | :--- | :--- | :--- |
| **`RandomSelectionBaseline`** | Facility Location / Stop Activation | Independent Bit-Sampling ($x_j \sim \mathcal{U}(0,1)$) | None (Relies entirely on Evaluator penalties) |
| **`RandomDepotBaseline`** | Traveling Salesperson (TSP) | Random Array Permutation / Shuffling | Hard-coded cyclic loop (Always starts/ends at same node) |
| **`RandomUAVBaseline`** | Capacitated Vehicle Routing (CVRP) | Uniform Random Choice from Feasible Subset | Hard cargo capacity filter ($q_j \le Q_{\text{left}}$) |