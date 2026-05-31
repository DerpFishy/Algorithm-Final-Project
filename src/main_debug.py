from data.debug_instance import customers, stops, depot
from ga_optimizer import GA
from visualization import plot_side_by_side

# run GA
ga = GA(customers, stops)
best, score, history = ga.run(generations=10)

print("Best solution:", best)
print("Best score:", score)

# optional: compare with random baseline
import random
random_sol = (
    [s["id"] for s in stops],  # simple route
    [random.randint(0, len(stops)-1) for _ in customers]
)

# visualize
plot_side_by_side(customers, stops, best, random_sol)