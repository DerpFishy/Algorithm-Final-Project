import random
from evaluator import evaluate_solution


def random_solution(customers, stops, trials=50):
    best = None
    best_score = float("inf")
    m = len(stops)

    for _ in range(trials):

        # ----------------------------
        # RANDOM BUT STRUCTURED ORDER
        # ----------------------------
        stop_order = list(range(m))
        random.shuffle(stop_order)

        # ----------------------------
        # STRUCTURED ASSIGNMENT (NOT PURE NOISE)
        # ----------------------------
        assignment = []
        for i in range(len(customers)):
            # biased random instead of full uniform chaos
            if random.random() < 0.7:
                assignment.append(i % m)
            else:
                assignment.append(random.randint(0, m - 1))

        chrom = (stop_order, assignment)

        score = evaluate_solution(chrom, customers, stops)

        if score < best_score:
            best_score = score
            best = chrom

    return best, best_score