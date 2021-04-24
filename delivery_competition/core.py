import collections
import os
import math
import random
import argparse
import sys


class TaskInput(object):
    def __init__(self, lines_i):
        lines_i = iter(lines_i)
        V, W, R, P, M, N = [int(x) for x in next(lines_i).strip().split(" ")]

        weights = [0 for _ in range(W)]
        vehicles = [0 for _ in range(V)]
        restaurant_location = [None for _ in range(R)]
        restaurant_goods = [set() for _ in range(R)]

        order_location = [None for _ in range(P)]
        order_goods = [None for _ in range(P)]

        for vid in range(V):
            vehicles[vid] = int(next(lines_i).strip())

        for wid in range(W):
            weights[wid] = int(next(lines_i).strip())

        for rid in range(R):
            data = [int(x) for x in next(lines_i).strip().split(" ")]
            restaurant_location[rid] = (data[0], data[1])
            goods = data[3:]
            goods_count = int(data[2])
            assert len(goods) == goods_count
            for j in goods:
                restaurant_goods[rid].add(j)

        GOODS_IN_RESTAURANTS = set(y for x in restaurant_goods for y in x)

        for pid in range(P):
            data = [int(x) for x in next(lines_i).strip().split(" ")]
            order_location[pid] = (data[0], data[1])
            order_goods[pid] = data[3:]
            assert all(x in GOODS_IN_RESTAURANTS for x in order_goods[pid]), "Incorrect input file"
            assert len(order_goods[pid]) == data[2]

        self.V = V
        self.W = W
        self.R = R
        self.P = P
        self.M = M
        self.N = N
        self.weights = weights
        self.vehicles = vehicles
        self.restaurant_location = restaurant_location
        self.restaurant_goods = restaurant_goods


        self.order_location = order_location
        self.order_goods = order_goods

    def evaluate(self, lines_o):
        lines_o = iter(lines_o)
        n = int(next(lines_o).strip())
        assert n <= self.V
        L = [0 for _ in range(self.R)]
        v_used = [False for x in range(self.V)]
        visited = [False for x in range(self.P)]
        total = 0
        for _ in range(n):
            v = int(next(lines_o).strip())
            assert not v_used[v]
            v_used[v] = True
            prev = (0, 0)
            weight = 0
            route_length = int(next(lines_o).strip())
            goods_in_bag = collections.defaultdict(int)
            for _ in range(route_length):
                line = [x for x in next(lines_o).strip().split(" ")]
                object_type = line[0]
                loc_id = int(line[1])
                if object_type == "R":
                    loc = self.restaurant_location[loc_id]
                elif object_type == "D":
                    loc = self.order_location[loc_id]
                else:
                    raise ValueError
                distance = mdist(prev, loc)
                prev = loc

                if object_type == "R":
                    goods = [int(x) for x in line[3:]]
                    for i in goods:
                        assert i < self.W
                        assert i in self.restaurant_goods[loc_id]
                        weight += self.weights[i]
                        goods_in_bag[i] += 1
                    assert weight <= self.vehicles[v]
                else:
                    for i in self.order_goods[int(line[1])]:
                        assert goods_in_bag[i] > 0
                        weight -= self.weights[i]
                        goods_in_bag[i] -= 1
                        visited[loc_id] = True
                total += distance
        assert all(visited), "You have to visit all the customers"
        return total

    def order_weight(self, order_id):
        return sum(self.weights[good_id] for good_id in self.order_goods[order_id])


def mdist(a, b):
    return abs(b[0] - a[0]) + abs(b[1] - a[1])


def pizza():
    random.seed(0)
    v = [2000 for _ in range(100)]
    v.extend(5000 for _ in range(50))
    V = len(v)
    N_shops = 20
    w = []

    j = 0
    shop_goods = collections.defaultdict(list)
    for i in range(N_shops):
        R = []
        R.extend([500] * random.randint(15, 25))
        R.extend([700] * random.randint(15, 25))
        R.extend([1000] * random.randint(2, 10))
        for x in R:
            shop_goods[i].append(j)
            j += 1
        w.extend(R)
    W = len(w)
    M = 1000
    N = 1000

    r = set((random.randint(1, M - 1), random.randint(1, N - 1)) for _ in range(100))
    R = len(r)
    p = set((random.randint(1, M - 1), random.randint(1, N - 1)) for _ in range(10000))
    p = [x for x in p if x not in r]
    P = len(p)
    O = [[] for _ in range(P)]

    for i in range(len(O)):
        shop_id = random.randint(0, N_shops - 1)
        goods = shop_goods[shop_id]
        O[i].extend(random.choice(goods) for _ in range(random.randint(1, 5)))

    print("Max order weight:", max(sum(w[y] for y in x) for x in O))

    rows = []
    rows.append(f"{V} {W} {R} {P} {M} {N}")

    for x in v:
        rows.append(str(x))

    r = list(r)
    random.shuffle(r)
    for x in w:
        rows.append(str(x))


    for shop_id in range(N_shops):
        coord = r[shop_id]
        goods = shop_goods[shop_id]
        rows.append(f"{coord[0]} {coord[1]} {len(goods)} {' '.join(str(x) for x in goods)}")

    for rid in range(N_shops, R):
        coord = r[rid]
        shop_id = random.randint(0, N_shops - 1)
        goods = shop_goods[shop_id]
        rows.append(f"{coord[0]} {coord[1]} {len(goods)} {' '.join(str(x) for x in goods)}")

    assert all(x in shop_goods for x in range(N_shops))

    GOODS_IN_RESTAURANTS= set(y for x in O for y in x)

    for pid in range(P):
        coord = p[pid]
        goods = O[pid]
        assert all(x in GOODS_IN_RESTAURANTS for x in goods)
        rows.append(f"{coord[0]} {coord[1]} {len(goods)} {' '.join(str(x) for x in goods)}")
    return "\n".join(rows)


def pizza2():
    random.seed(1)
    v = [2000 for _ in range(100)]
    v.extend(5000 for _ in range(25))
    v.extend(10000 for _ in range(25))
    V = len(v)
    N_shops = 20
    w = []

    j = 0
    shop_goods = collections.defaultdict(list)
    for i in range(N_shops):
        R = []
        R.extend([500] * random.randint(15, 25))
        R.extend([700] * random.randint(15, 25))
        R.extend([1000] * random.randint(2, 10))
        for x in R:
            shop_goods[i].append(j)
            j += 1
        w.extend(R)
    W = len(w)
    M = 1000
    N = 1000

    r = set((random.randint(1, M - 1), random.randint(1, N - 1)) for _ in range(100))
    R = len(r)
    p = set((random.randint(1, M - 1), random.randint(1, N - 1)) for _ in range(10000))
    p = [x for x in p if x not in r]
    P = len(p)
    O = [[] for _ in range(P)]

    for i in range(len(O)):
        shops_count = random.randint(1, 5)
        shops = list(range(N_shops))
        random.shuffle(shops)
        shops = shops[:shops_count]
        O[i].extend(random.choice(shop_goods[shop_id]) for shop_id in shops)

    print("Max order weight:", max(sum(w[y] for y in x) for x in O))

    rows = []
    rows.append(f"{V} {W} {R} {P} {M} {N}")

    for x in v:
        rows.append(str(x))

    r = list(r)
    random.shuffle(r)
    for x in w:
        rows.append(str(x))

    for shop_id in range(N_shops):
        coord = r[shop_id]
        goods = shop_goods[shop_id]
        rows.append(f"{coord[0]} {coord[1]} {len(goods)} {' '.join(str(x) for x in goods)}")

    for rid in range(N_shops, R):
        coord = r[rid]
        shop_id = random.randint(0, N_shops - 1)
        goods = shop_goods[shop_id]
        rows.append(f"{coord[0]} {coord[1]} {len(goods)} {' '.join(str(x) for x in goods)}")
    assert all(x in shop_goods for x in range(N_shops))

    GOODS_IN_RESTAURANTS= set(y for x in O for y in x)

    for pid in range(P):
        coord = p[pid]
        goods = O[pid]
        assert all(x in GOODS_IN_RESTAURANTS for x in goods)
        rows.append(f"{coord[0]} {coord[1]} {len(goods)} {' '.join(str(x) for x in goods)}")
    return "\n".join(rows)


def real_life():
    random.seed(2)
    v = [2000 for _ in range(100)]
    v.extend(5000 for _ in range(25))
    v.extend(10000 for _ in range(15))
    v.extend(20000 for _ in range(15))
    v.extend(40000 for _ in range(12))
    v.extend(100000 for _ in range(10))
    V = len(v)
    N_shops = 50
    w = []

    j = 0
    shop_goods = collections.defaultdict(list)
    for i in range(N_shops):
        R = []
        R.extend([random.randint(250, 500)] * random.randint(15, 25))
        R.extend([random.randint(500, 750)] * random.randint(15, 25))
        R.extend([random.randint(1000, 1250)] * random.randint(2, 10))
        R.extend([random.randint(2000, 2250)] * random.randint(2, 10))
        R.extend([random.randint(4000, 12250)] * random.randint(2, 5))
        for x in R:
            shop_goods[i].append(j)
            j += 1
        w.extend(R)
    W = len(w)
    M = 1000
    N = 1000

    r = set((random.randint(1, M - 1), random.randint(1, N - 1)) for _ in range(100))
    R = len(r)
    p = set((random.randint(1, M - 1), random.randint(1, N - 1)) for _ in range(10000))
    p = [x for x in p if x not in r]
    P = len(p)
    O = [[] for _ in range(P)]

    for i in range(len(O)):
        shops_count = random.randint(1, 5)
        shops = list(range(N_shops))
        random.shuffle(shops)
        shops = shops[:shops_count]
        counts = [random.randint(1, 4) for x in shops]
        O[i].extend(random.choice(shop_goods[shop_id]) for count, shop_id in zip(counts, shops) for _ in range(count))

    print("Max order weight:", max(sum(w[y] for y in x) for x in O))

    rows = []
    rows.append(f"{V} {W} {R} {P} {M} {N}")

    for x in v:
        rows.append(str(x))

    r = list(r)
    random.shuffle(r)
    for x in w:
        rows.append(str(x))

    for shop_id in range(N_shops):
        coord = r[shop_id]
        goods = shop_goods[shop_id]
        rows.append(f"{coord[0]} {coord[1]} {len(goods)} {' '.join(str(x) for x in goods)}")

    for rid in range(N_shops, R):
        coord = r[rid]
        shop_id = random.randint(0, N_shops - 1)
        goods = shop_goods[shop_id]
        rows.append(f"{coord[0]} {coord[1]} {len(goods)} {' '.join(str(x) for x in goods)}")
    assert all(x in shop_goods for x in range(N_shops))

    GOODS_IN_RESTAURANTS= set(y for x in O for y in x)

    for pid in range(P):
        coord = p[pid]
        goods = O[pid]
        assert all(x in GOODS_IN_RESTAURANTS for x in goods)
        rows.append(f"{coord[0]} {coord[1]} {len(goods)} {' '.join(str(x) for x in goods)}")
    return "\n".join(rows)


def main():
    parser = argparse.ArgumentParser(description="Discrete optimization problem")
    parser.add_argument("--input", "-i", type=str, required=True, help="Input file for the task")
    parser.add_argument("--output", "-o", type=str, required=True, help="Solution for the task")
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Cannot access '{args.input}': No such file", file=sys.stder)
        sys.exit(1)

    if not os.path.exists(args.output):
        print(f"Cannot access '{args.input}': No such file", file=sys.stder)
        sys.exit(2)

    with open(args.input) as fp:
        task_input = TaskInput(fp)

    with open(args.output) as fp:
        print(f"Solution {args.output} for {args.input}")
        try:
            print("Score: ", task_input.evaluate(fp))
        except Exception as e:
            print("Invalid output format: ", str(e))
