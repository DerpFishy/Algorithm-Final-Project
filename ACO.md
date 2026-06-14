# 1. Depot ACO: Mathematical Formulation

The `DepotACO` algorithm optimizes a path through a set of depots. It can be modeled as a **Traveling Salesperson Problem (TSP)** formulation optimized via an Ant Colony System.

### A. Sets and Core Parameters
* $S = \{0, 1, \dots, n-1\}$ : The set of depots.
* $d_{ij}$ : The distance between depot $i$ and depot $j$.
* $\tau_{ij}(t)$ : The amount of pheromone on the edge connecting depot $i$ and $j$ at iteration $t$.
* $\eta_{ij}$ : The visibility (heuristic value) of the edge from depot $i$ to $j$, defined as:
  $$\eta_{ij} = \frac{1}{d_{ij} + \epsilon} \quad \text{where } \epsilon = 10^{-9}$$

---

### B. State Transition Rule (Node Selection)
When an ant is at depot $i$, the probability $p_{ij}$ of choosing to move to an unvisited depot $j \in \text{unvisited}$ is given by:

$$p_{ij} = \frac{[\tau_{ij}]^\alpha \cdot [\eta_{ij}]^\beta}{\sum_{k \in \text{unvisited}} [\tau_{ik}]^\alpha \cdot [\eta_{ik}]^\beta}$$

* $\alpha$ balances the weight of historical pheromone deposits.
* $\beta$ balances the weight of local distance heuristics.

---

### C. Pheromone Evolution Rule
At the end of an iteration, pheromone values are adjusted across the network in a two-stage process:

1. **Evaporation:** Every edge undergoes pheromone degradation governed by evaporation rate $\rho \in [0, 1]$:
   $$\tau_{ij} \leftarrow (1 - \rho)\tau_{ij}$$

2. **Deposit:** Every ant $k \in \{1, \dots, m\}$ deposits a piece of pheromone on its traveled route, inversely proportional to its total tour cost $C_k$:
   $$\tau_{ij} \leftarrow \tau_{ij} + \sum_{k=1}^{m} \Delta \tau_{ij}^k$$
   
   $$\Delta \tau_{ij}^k = \begin{cases} \frac{1}{C_k + \epsilon} & \text{if edge } (i,j) \text{ belongs to route } k \\ 0 & \text{otherwise} \end{cases}$$

---
---

# 2. UAV ACO (ACOOnly): Mathematical Formulation

The `ACOOnly` class represents a **Capacitated Vehicle Routing Problem (CVRP)** where a fleet of UAVs serves a set of customers from a central depot.

### A. Sets, Capacity Constraints, and Heuristics
* $C = \{1, 2, \dots, n-1\}$ : The set of customers.
* $\{0\}$ : The designated central depot.
* $q_j$ : The cargo demand of customer $j$.
* $Q_{\max}$ : The maximum payload capacity of a single UAV.
* $\mathcal{F}(i, Q_{\text{left}})$ : The set of feasible next customers from current node $i$, given remaining cargo capacity $Q_{\text{left}}$:
  $$\mathcal{F}(i, Q_{\text{left}}) = \{ j \in \text{unvisited} \mid q_j \le Q_{\text{left}} \}$$

---

### B. $\epsilon$-Greedy State Transition Rule
To prevent premature stagnation, this implementation blends stochastic exploration with the classic ACO probability distribution. When an ant chooses a customer from node $i$:

$$j = \begin{cases} 
\text{Random selection from } \mathcal{F}(i, Q_{\text{left}}) & \text{with probability } 0.1 \\
\text{Sampled from distribution } P_{ij} & \text{with probability } 0.9 
\end{cases}$$

Where the structural transition probability distribution $P_{ij}$ over the feasible neighborhood is:

$$P_{ij} = \frac{[\tau_{ij}]^\alpha \cdot [\eta_{ij}]^\beta}{\sum_{k \in \mathcal{F}(i, Q_{\text{left}})} [\tau_{ik}]^\alpha \cdot [\eta_{ik}]^\beta}$$

---

### C. Elitist (Ranked) Pheromone Update Rule
Unlike the standard global update, your UAV implementation applies a **Ranked/Elitist Pheromone Strategy** using only the top $20\%$ best ants.

Let $A_{\text{ranked}}$ be the subset of the top $K$ best solutions found in the current iteration, sorted by lowest total fleet route cost $C_s$:

$$K = \max\left(1, \left\lfloor \frac{m}{5} \right\rfloor\right)$$

1. **Evaporation:** Applied globally across all node links:
   $$\tau_{ij} \leftarrow (1 - \rho)\tau_{ij}$$

2. **Symmetric Elite Deposit:** Pheromone is reinforced symmetrically along both directed pathways $(a,b)$ and $(b,a)$ for every individual route within an elite solution $s \in A_{\text{ranked}}$:
   $$\tau_{ab} \leftarrow \tau_{ab} + \frac{1}{C_s + \epsilon}, \quad \tau_{ba} \leftarrow \tau_{ba} + \frac{1}{C_s + \epsilon} \quad \forall (a,b) \in s$$