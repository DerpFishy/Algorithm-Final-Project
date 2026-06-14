# Multi-Tier Logistics Optimization Suite: Technical Report
This report provides the complete documentation, mathematical formulations, configuration baselines, and performance analysis for our multi-tier logistics optimization framework.

---

## 1. Problem Introduction & Domains
The optimization suite decouples a complex, heavy-infrastructure logistics network challenge into three distinct mathematical problem domains:

1. **Stop Selection & Customer Assignment Domain:** Modeled as a variant of the **Uncapacitated Facility Location Problem (UFLP)**. It balances the operational costs of maintaining transit or delivery facilities against customer distance convenience.
2. **Depot Routing Domain:** Modeled as a classic **Traveling Salesperson Problem (TSP)** to find the shortest cyclic ground route connecting active facilities.
3. **UAV Payload Delivery Domain:** Modeled as a **Capacitated Vehicle Routing Problem (CVRP)**, handling last-mile aerial delivery from facilities to payload-constrained customers.

---

## 2. Mathematical Formulations

### A. Phase 1: Stop Selection and Customer Assignment (UFLP)
Let $S = \{1, 2, \dots, |S|\}$ be the set of potential stops indexed by $j$, and $C = \{1, 2, \dots, |C|\}$ be the set of customers indexed by $i$. 

#### Decision Variables
The Genetic Algorithm uses a binary configuration vector (chromosome) $\mathbf{x} = [x_1, x_2, \dots, x_{|S|}]$, where:
$$x_j = \begin{cases} 1 & \text{if stop } j \text{ is open} \\ 0 & \text{otherwise} \end{cases}$$

#### Objective Function (Fitness Evaluation)
The objective minimizes the total system cost $f(\mathbf{x})$, comprising customer travel distances, facility configuration weights, and penalties for under-utilization:
$$\min_{\mathbf{x}} \quad f(\mathbf{x}) = T(\mathbf{x}) + F(\mathbf{x}) + P(\mathbf{x})$$

Where individual sub-components are defined as:
* **Total Customer Distance Cost $T(\mathbf{x})$:**
  $$d_i^*(\mathbf{x}) = \min_{j \in S: x_j = 1} d_{ij}$$
  $$\text{DistancePenalty}(d) = \begin{cases} 0 & \text{if } d \le D_{\max} \\ 10 \cdot (d - D_{\max}) & \text{if } d > D_{\max} \end{cases}$$
  $$T(\mathbf{x}) = \frac{1}{|C|} \sum_{i \in C} \left( d_i^*(\mathbf{x}) + \text{DistancePenalty}\big(d_i^*(\mathbf{x})\big) \right)$$
* **Facility Configuration Cost $F(\mathbf{x})$:**
  $$F(\mathbf{x}) = \alpha \sqrt{\sum_{j \in S} x_j}$$
* **Unused Open Stop Penalty $P(\mathbf{x})$:** Let $U(\mathbf{x})$ define open stops failing to capture customer assignments:
  $$U(\mathbf{x}) = \left\{ j \in S \;\middle|\; x_j = 1 \;\land\; \forall i \in C, \, j \neq \arg\min_{k \in S: x_k = 1} d_{ik} \right\}$$
  $$P(\mathbf{x}) = 5.0 \cdot |U(\mathbf{x})|$$

---

### B. Phase 2: Depot Routing (TSP)
Optimizes a cyclic path through active depots $S_{\text{active}} \subset S$ via an Ant Colony System.
* **Visibility Heuristic:** $\eta_{ij} = \frac{1}{d_{ij} + \epsilon} \quad \text{where } \epsilon = 10^{-9}$
* **State Transition Probability:** The probability $p_{ij}$ of an ant moving from depot $i$ to unvisited depot $j$:
  $$p_{ij} = \frac{[\tau_{ij}]^\alpha \cdot [\eta_{ij}]^\beta}{\sum_{k \in \text{unvisited}} [\tau_{ik}]^\alpha \cdot [\eta_{ik}]^\beta}$$
* **Global Pheromone Update Rule:**
  $$\tau_{ij} \leftarrow (1 - \rho)\tau_{ij} + \sum_{k=1}^{m} \Delta \tau_{ij}^k$$
  $$\Delta \tau_{ij}^k = \begin{cases} \frac{1}{C_k + \epsilon} & \text{if edge } (i,j) \text{ belongs to route } k \\ 0 & \text{otherwise} \end{cases}$$

---

### C. Phase 3: UAV Last-Mile Delivery (CVRP)
Optimizes aerial routes departing and returning to an active facility under strict capacity rules.
* **Feasible Neighborhood Filter:** $\mathcal{F}(i, Q_{\text{left}}) = \{ j \in \text{unvisited} \mid q_j \le Q_{\text{left}} \}$
* **$\epsilon$-Greedy Transition Rule:** To balance exploration, next node selection follows:
  $$j = \begin{cases} \text{Random selection from } \mathcal{F}(i, Q_{\text{left}}) & \text{with probability } 0.1 \\ \text{Sampled from distribution } P_{ij} & \text{with probability } 0.9 \end{cases}$$
  $$P_{ij} = \frac{[\tau_{ij}]^\alpha \cdot [\eta_{ij}]^\beta}{\sum_{k \in \mathcal{F}(i, Q_{\text{left}})} [\tau_{ik}]^\alpha \cdot [\eta_{ik}]^\beta}$$
* **Ranked Elitist Pheromone Reinforcement:** Applied using only the top $K$ best solutions ($A_{\text{ranked}}$):
  $$K = \max\left(1, \left\lfloor \frac{m}{5} \right\rfloor\right)$$
  $$\tau_{ab} \leftarrow (1-\rho)\tau_{ab} + \frac{1}{C_s + \epsilon}, \quad \tau_{ba} \leftarrow (1-\rho)\tau_{ba} + \frac{1}{C_s + \epsilon} \quad \forall (a,b) \in s \in A_{\text{ranked}}$$

---

## 3. Stochastic Random Baselines

To benchmark metaheuristic efficiency, three pure random controls were built to map out performance floors:

1. **`RandomSelectionBaseline`:** Assigns uniform binary configurations via independent bit-sampling $x_j \sim \mathcal{U}_{\text{discrete}}(0, 1)$ to test facility placement vs. the GA.
2. **`RandomDepotBaseline`:** Constructs a random permutation sequence $\sigma$ from remaining depots to build a complete cyclic loop vector $\mathbf{R} = [d_{\text{start}}, r_1, \dots, r_{n-1}, d_{\text{start}}]$ to test the TSP performance.
3. **`RandomUAVBaseline`:** Sequentially drafts capacity-compliant last-mile paths by sampling destinations uniformly from a dynamically filtered constraint subset: $nxt \sim \mathcal{U}_{\text{discrete}}\left(\mathcal{F}(Q_{\text{left}})\right)$.

---

## 4. Hyperparameter Configuration Matrix

| Algorithm Component | Parameter Definition | Variable / Rule | Configured Value |
| :--- | :--- | :--- | :--- |
| **GAOnly** | Population Size | $N$ | $\max(30, \min(500, 10 \cdot \vert S \vert))$ |
| | Elite Size | $N_e$ | $\max(2, \lfloor N / 10 \rfloor)$ |
| | Mutation Rate / Crossover | $r_m \; / \; p_c$ | $0.3 \; / \; 0.5$ |
| **Evaluator** | Max Distance Threshold | $D_{\max}$ | $1.0$ |
| | Distance Penalization Weight | Linear Multiplier | $10.0$ |
| | Facility Structural Weight | $\alpha$ | $1.0$ |
| | Unused Stop Penalty | Fixed Cost Component | $5.0$ |
| **DepotACO** | Ant Count / Evaporation | $m \; / \; \rho$ | $10 \; / \; 0.2$ |
| | Pheromone / Heuristic Weights | $\alpha \; / \; \beta$ | $1.5 \; / \; 1.5$ |
| **ACOOnly** | Fleet Exploration Rate | Stochastic Chance | $0.1$ |
| | Pheromone Ranking Cut-off | Top Performers ($K$) | $\max(1, \lfloor m / 5 \rfloor)$ (Top $20\%$) |

---

## 5. Experimental Architecture & Control Flow

The `run_experiment` module coordinates tasks across three decoupled execution layers to map global costs out over four experimental variants:

    [Input Coordinates, Capacity, Speeds]
    │
    ▼
    ┌───────────────────────────────┐
    │   Phase 1: Facility Location  │ ──► Evaluates Allocation
    │     (GAOnly vs. RandomSB)     │
    └───────────────┬───────────────┘
    │
    ├──────────────────────────────────────┐
    ▼ (GA Snapshot Clusters)               ▼ (Random Baseline Clusters)
    ┌───────────────────────────────┐      ┌───────────────────────────────┐
    │   Phase 2: Inter-Depot Route  │      │   Phase 2: Inter-Depot Route  │
    │  (Hybrid ACO vs. GA Baseline) │      │  (Random ACO vs. True Random) │
    └───────────────┬───────────────┘      └───────────────┬───────────────┘
    │ ──► Solves TSP                       │ ──► Solves TSP
    ▼ (Scaled via truck_V)                 ▼ (Scaled via truck_V)
    ┌───────────────────────────────┐      ┌───────────────────────────────┐
    │   Phase 3: Last-Mile Fleet    │      │   Phase 3: Last-Mile Fleet    │
    │ (ACOOnly vs. Random Baseline) │      │ (ACOOnly vs. Random Baseline) │
    └───────────────┬───────────────┘      └───────────────┬───────────────┘
    │ ──► Solves CVRP                      │ ──► Solves CVRP
    ▼ (Scaled via UAV_V)                   ▼ (Scaled via UAV_V)
