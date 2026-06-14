# Experimental Datasets

The benchmark datasets are defined as

$$
D_k = (C_k, S_k, Q_{\max}, V, R),
\qquad k \in \{1,2,3\}
$$

where

$$
C_k=\{(x_i,y_i,q_i)\mid i=1,\ldots,n\}
$$

is the set of customer locations and demands, and

$$
S_k=\{(x_j,y_j)\mid j=1,\ldots,m\}
$$

is the set of candidate truck-stop locations.

## Common Parameters

$$
Q_{\max}=15,
\qquad
V=100,
\qquad
R=50
$$

$$
|C_k|=10,
\qquad
|S_k|=3,
\qquad
\forall k\in\{1,2,3\}
$$

## Dataset Summary

$$
\begin{aligned}
D_1 &: \text{Mixed Clusters},\\
D_2 &: \text{Radial Spread},\\
D_3 &: \text{Random Balanced Field}
\end{aligned}
$$

## Dataset Characteristics

$$
D_1:\;
\text{Clustered customer groups with scattered outliers}
$$

$$
D_2:\;
\text{Radially distributed customers around a central region}
$$

$$
D_3:\;
\text{Uniformly distributed customers across the service area}
$$