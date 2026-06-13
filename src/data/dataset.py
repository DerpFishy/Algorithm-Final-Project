import random

def generate_random_dataset(num_customers, num_stops, truckV, UAVV,
                             seed=None):

    if seed is not None:
        random.seed(seed)

    customers = []
    stops = []

    districts = [
        (2000, 2000),
        (8000, 2000),
        (2000, 8000),
        (8000, 8000),
        (5000, 5000),
    ]

    cid = 0

    # ~30 customers per district
    for cx, cy in districts:

        for _ in range(num_customers // len(districts)):

            customers.append({
                "id": cid,
                "x": max(0, min(10000, int(random.gauss(cx, 700)))),
                "y": max(0, min(10000, int(random.gauss(cy, 700)))),
                "q": random.randint(1, 5)
            })

            cid += 1

    customers[0]["q"] = 0

    # candidate stops
    for sid in range(num_stops):

        stops.append({
            "id": sid,
            "x": random.randint(0, 10000),
            "y": random.randint(0, 10000)
        })

    Qmax = 15
    truck_V = truckV * 100
    UAV_V = UAVV * 100

    return customers, stops, Qmax, truck_V, UAV_V