# Mathematical Formulation of the Genetic Algorithm
## 1. Sets and Indices
* $S = \{1, 2, \dots, |S|\}$ : Set of potential **stops** (indexed by $j$).
* $C = \{1, 2, \dots, |C|\}$ : Set of **customers** (indexed by $i$).

## 2. Decision Variables
The Genetic Algorithm uses a binary chromosome representing the activation state of each stop. Let the decision vector (chromosome) be $\mathbf{x} = [x_1, x_2, \dots, x_{|S|}]$, where:

$$x_j = \begin{cases} 1 & \text{if stop } j \text{ is open} \\ 0 & \text{otherwise} \end{cases}$$

---

## 3. The Objective Function (Fitness)
The objective is to find a configuration vector $\mathbf{x}$ that minimizes the total cost function $f(\mathbf{x})$, comprising customer travel distances, facility configuration weights, and penalties for under-utilization:

$$\min_{\mathbf{x}} \quad f(\mathbf{x}) = T(\mathbf{x}) + F(\mathbf{x}) + P(\mathbf{x})$$

Where the individual components are defined as follows:

### A. Total Customer Distance Cost $T(\mathbf{x})$
Each customer $i$ maps dynamically to their nearest open stop. The shortest distance $d_i^*(\mathbf{x})$ for customer $i$ given the active stops is:

$$d_i^*(\mathbf{x}) = \min_{j \in S: x_j = 1} d_{ij}$$

Where $d_{ij}$ is the distance between customer $i$ and stop $j$. 

If this distance exceeds a maximum threshold $D_{\max}$ (where $D_{\max} = 1$), a linear penalty with a multiplier of $10$ is applied. The distance cost function for an individual distance $d$ is:

$$\text{DistancePenalty}(d) = \begin{cases} 0 & \text{if } d \le D_{\max} \\ 10 \cdot (d - D_{\max}) & \text{if } d > D_{\max} \end{cases}$$

The total service cost $T(\mathbf{x})$ is the arithmetic mean of the penalized distances across all customers:

$$T(x) = \frac{1}{|C|} \sum_{i \in C} ( A_i + B_i )$$

$$where \quad A_i = d^{*}_{i}(x), \quad B_i = \mathrm{DistancePenalty}(A_i)$$

### B. Facility Cost $F(\mathbf{x})$
The structural cost of opening facilities scales sub-linearly with respect to the total number of open stops, governed by a control parameter $\alpha$ (where $\alpha = 1$):

$$F(\mathbf{x}) = \alpha \sqrt{\sum_{j \in S} x_j}$$

### C. Unused Open Stop Penalty $P(\mathbf{x})$
Let $U(\mathbf{x})$ define the set of open stops that fail to capture any customer assignments (i.e., they are open but are never the closest stop for any customer):

$$U(\mathbf{x}) = \{ j \in S \mid x_j = 1 \land \forall i \in C,\; j \ne \arg\min_{k \in S,\; x_k = 1} d_{ik} \}$$

A constant penalty of $5.0$ is levied on each wasteful, unused stop:

$$P(\mathbf{x}) = 5.0 \cdot |U(\mathbf{x})|$$

---

## 4. Genetic Operators

Let $P^{(t)} = \{\mathbf{x}^{(1)}, \mathbf{x}^{(2)}, \dots, \mathbf{x}^{(N)}\}$ denote the population of size $N$ at generation $t$.

### Selection
Tournament selection chooses a subset $K$ of size $k=5$ uniformly at random from the population:
$$K \subset P^{(t)}, \quad |K| = k$$

The individual with the lowest objective value wins the tournament slot:
$$\mathbf{x}_{\text{selected}} = \arg\min_{\mathbf{x} \in K} f(\mathbf{x})$$

### Crossover
Given selected parents $\mathbf{p_1}$ and $\mathbf{p_2}$, uniform crossover constructs a child chromosome $\mathbf{c}$ gene-by-gene via a Bernoulli process:

$$c_i = \begin{cases} p_{1,i} & \text{with probability } 0.5 \\ p_{2,i} & \text{with probability } 0.5 \end{cases} \quad \forall i \in \{1, \dots, |S|\}$$

### Mutation & Constraints
Each gene in $\mathbf{c}$ undergoes a bitwise mutation (XOR operation) with a mutation probability rate $r_m = 0.3$:

$$c_i \leftarrow c_i \oplus Y_i, \quad \text{where } Y_i \sim \text{Bernoulli}(r_m)$$

**Feasibility Correction:** To prevent an empty network configuration, the following constraint enforcement rule is evaluated:

$$\text{If } \sum_{i=1}^{|S|} c_i = 0, \quad \text{then } c_j \leftarrow 1 \quad \text{where } j \sim \mathcal{U}(1, |S|)$$