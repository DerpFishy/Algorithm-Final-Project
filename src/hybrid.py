# Algorithm 3: Hybrid GA + ACO (Proposed Method)

# Input:
#     Customers C
#     Candidate Stops S
#     GA parameters
#     ACO parameters

# Output:
#     Best global solution

# Begin

#     Initialize GA population:
#         Chromosome = (y_s, x_i^s)

#     For generation = 1 to G do:

#         // --------------------------
#         // GA PHASE (GLOBAL SEARCH)
#         // --------------------------

#         For each chromosome:
#             Decode:
#                 Assign customers to selected stops
#             End

#             For each active stop s:
#                 Form cluster C_s

#                 Apply ACO:
#                     route_s, cost_s = ACO(H_s, C_s)

#             Total cost = sum of all cluster costs

#         End

#         Select elite chromosomes

#         Apply crossover + mutation:
#             - stop selection mutation (y_s)
#             - assignment mutation (x_i^s)

#         // --------------------------
#         // HYBRID REFINEMENT
#         // --------------------------

#         For elite individuals:
#             Re-run ACO on clusters
#             Update cost with improved routes

#         End

#     End For

#     Return best (y_s, x_i^s) + ACO routes

# End

# GA evolves structure
# FOR each individual:
#     split into clusters
#     run ACO per cluster
#     compute cost
# selection + mutation
# repeat
# return best