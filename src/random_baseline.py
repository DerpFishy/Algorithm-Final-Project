import random
from evaluator import evaluate_solution
from aco_optimizer import ACO

def random_solution(customers, stops, aco, trials=50):
    best = None
    best_score = float("inf")

    for _ in range(trials):
        stop_order = [s["id"] for s in stops]
        random.shuffle(stop_order)

        assignment = [
            random.randint(0, len(stops)-1)
            for _ in customers
        ]

        chrom = (stop_order, assignment)

        score = evaluate_solution(chrom, customers, stops, aco)

        if score < best_score:
            best_score = score
            best = chrom

    return best, best_score