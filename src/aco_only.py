# Algorithm 2: Ant Colony Optimization (ACO Only)

# Input:
#     Customers C
#     Depot / starting hub H
#     Distance matrix D
#     Number of ants A
#     Iterations T

# Output:
#     Best route

# Begin

#     Initialize pheromone matrix τ(i,j) = constant

#     For iteration = 1 to T do:

#         For each ant k = 1 to A do:

#             Start at hub H
#             Unvisited = all customers

#             Route = [H]

#             While Unvisited is not empty do:

#                 For each candidate j in Unvisited:
#                     Compute probability:
#                         P(i,j) ∝ [τ(i,j)]^α * [1/d(i,j)]^β

#                 Select next node probabilistically
#                 Move to node j
#                 Add j to Route
#                 Remove j from Unvisited

#             End While

#             Return to H
#             Compute route cost

#         End For

#         Update pheromones:
#             Evaporate: τ = (1 - ρ) * τ
#             Deposit: better routes add pheromone

#     End For

#     Return best route found

# End

# Initialize pheromone
# For each ant
#     build route
# update pheromone
# return best route