import random

def generate_random_dataset(num_customers, num_stops, truckV, UAVV,
                             seed=None):

    if seed is not None:
        random.seed(seed)

    customers = []
    stops = []

    districts = [
        (3, 3),
        (3, 12),
        (7.5, 7.5),
        (12, 12),
        (12, 3)
    ]

    cid = 0

    # customers per district
    for cx, cy in districts:

        for _ in range(num_customers // len(districts)):

            customers.append({
                "id": cid,
                "x": max(0, min(15, round(random.gauss(cx, 1), 3))),
                "y": max(0, min(15, round(random.gauss(cy, 1), 3))),
                "q": random.randint(1, 5)
            })

            cid += 1

    # candidate stops
    sid = 0
    for sx, sy in districts:

        for _ in range(num_stops // len(districts)):

            stops.append({
                "id": sid,
                "x": max(0, min(15, round(random.gauss(sx, 3), 3))),
                "y": max(0, min(15, round(random.gauss(sy, 3), 3)))
            })

            sid += 1

    Qmax = 15
    truck_V = truckV
    UAV_V = UAVV

    return customers, stops, Qmax, truck_V, UAV_V