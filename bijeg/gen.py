#!/usr/bin/python2

from queue import PriorityQueue
import math
import subprocess
import random
import os
import glob
import sys
doc = """
  Cenerate all test cases in test/:  gen.py
"""


PROBLEM = "bijeg"
sys.setrecursionlimit(1000010)


def dijkstra(src, G):
    dist = [-1] * len(G)
    pq = PriorityQueue()
    pq.put((0, src))
    while not pq.empty():
        (curr_d, node) = (-1, -1)
        while not pq.empty():
            (curr_d, node) = pq.get()
            if dist[node] == -1:
                break
            (curr_d, node) = (-1, -1)
        if curr_d == -1:
            break
        dist[node] = curr_d
        for (nxt, nxt_d) in G[node]:
            if dist[nxt] != -1:
                continue
            pq.put((curr_d + nxt_d, nxt))

    return dist


class Test(object):
    def __init__(self, n, m, k, es, qs):
        self.n = n   # number of nodes
        self.m = m   # number of edges
        self.k = k   # number of queries
        self.es = es  # edges
        self.qs = qs  # queries

    def no_contradictions(self, G, spec_edges):
        d_root = dijkstra(0, G)
        for di in d_root:
            assert(di >= 0)

        piv = 0
        for (a, b, _) in spec_edges:
            if d_root[a] > d_root[piv]:
                piv = a
            if d_root[b] > d_root[piv]:
                piv = b

        d_piv = dijkstra(piv, G)

        for (a, b, d) in spec_edges:
            assert(d_root[piv] == d_root[a] + d + d_piv[b] or
                   d_root[piv] == d_root[b] + d + d_piv[a])

        ok = False
        for qi in self.qs:
            qi -= 1
            ok |= d_root[qi] == d_root[piv] + d_piv[qi]

        assert(ok)
        return True

    def validate(self):
        assert(2 <= self.n <= 10**5)
        assert(1 <= self.m <= 5 * (10**5))
        assert(1 <= self.k <= self.n)

        assert(len(self.es) == self.m)

        E = []
        V = [[] for _ in range(self.n)]

        spec_edges = []

        for (a, b, d, x) in self.es:
            assert(1 <= a <= self.n)
            assert(1 <= b <= self.n)
            assert(1 <= d <= 10 ** 9)
            assert(x in [0, 1])
            assert(a != b)
            E.append((min(a, b), max(a, b)))
            a -= 1
            b -= 1
            V[a].append((b, d))
            V[b].append((a, d))
            if x == 1:
                spec_edges.append((min(a, b), max(a, b), d))

        assert(len(set(E)) == self.m)
        assert(len(spec_edges) >= 1)

        assert(len(self.qs) == self.k)
        for qi in self.qs:
            assert(1 <= qi <= self.n)

        assert(self.no_contradictions(V, spec_edges))

    def write(self, fd=sys.stdout):
        print>>fd, self.n, self.m, self.k
        for (a, b, d, x) in self.es:
            print>>fd, a, b, d, x
        print>>fd, ' '.join(list(map(str, self.qs)))


def remove_cases():
    cases = glob.glob('test/%s.dummy.in.*' % PROBLEM)
    cases += glob.glob('test/%s.dummy.out.*' % PROBLEM)
    cases += glob.glob('test/%s.in.*' % PROBLEM)
    cases += glob.glob('test/%s.out.*' % PROBLEM)
    for c in cases:
        print>>sys.stderr, 'Removing ' + c
        os.remove(c)


def gen_rand(n, m, k, ones, d_hi):
    e_set = set()
    es = []
    G = [[] for _ in range(n)]

    for b in range(2, n + 1):
        a = random.randint(max(1, b - 50), b - 1)
        d = random.randint(1, d_hi)
        e_set.add((min(a, b), max(a, b)))
        es.append((a, b, d, 0))
        G[a - 1].append((b - 1, d))
        G[b - 1].append((a - 1, d))

    while len(es) != m:
        a = random.randint(1, n)
        b = random.randint(1, n)
        d = random.randint(1, d_hi)
        if (min(a, b), max(a, b)) in e_set or a == b:
            continue
        e_set.add((min(a, b), max(a, b)))
        es.append((a, b, d, 0))
        a -= 1
        b -= 1
        G[a].append((b, d))
        G[b].append((a, d))

    d_root = dijkstra(0, G)

    sd = sorted([(b, a) for (a, b) in enumerate(d_root)])
    c, piv = -1, -1
    for _ in range(5):
        curr_piv = sd[random.randint(10, n//9)][1]
        d_piv = dijkstra(curr_piv, G)
        cnt = 0
        for (a, b, d, _) in es:
            a -= 1
            b -= 1
            if d_root[curr_piv] == d_root[a] + d + d_piv[b] or d_root[curr_piv] == d_root[b] + d + d_piv[a]:
                cnt += 1
        (c, piv) = max((c, piv), (cnt, curr_piv))

    d_piv = dijkstra(piv, G)
    print("c: " + str(c) + ", piv: " + str(piv))

    one_set = set()
    for (a, b, d, _) in es:
        a -= 1
        b -= 1
        if (a == piv or b == piv) and (d_root[piv] == d_root[a] + d + d_piv[b] or d_root[piv] == d_root[b] + d + d_piv[a]):
            one_set.add((min(a, b) + 1, max(a, b) + 1))
            ones -= 1
            break

    if ones != 0: ones = c // 2
    for (a, b, d, _) in es:
        a -= 1
        b -= 1
        if ones > 0 and (d_root[piv] == d_root[a] + d + d_piv[b] or d_root[piv] == d_root[b] + d + d_piv[a]):
            one_set.add((min(a, b) + 1, max(a, b) + 1))
            ones -= 1

    es_final = []
    for (a, b, d, x) in es:
        if (min(a, b), max(a, b)) in one_set:
            es_final.append((a, b, d, 1))
        else:
            es_final.append((a, b, d, 0))

    A, B = [], []
    for node in range(1, n):
        if d_root[piv] + d_piv[node] == d_root[node]:
            B.append(node + 1)
        else:
            A.append(node + 1)

    print(len(A), len(B))

    qs = []
    if k != n - 1:
        qs = [piv + 1]
        for _ in range(k - 1):
            if random.randint(1, 2) == 1:
                qs.append(A[random.randint(0, len(A) - 1)])
            else:
                qs.append(B[random.randint(0, len(B) - 1)])
    else:
        qs = [x for x in range(2, n + 1)]

    return Test(n, m, k, es_final, qs)


def gen_cases():
    remove_cases()

    real = []
    dummy = []

    dummy.append(Test(
        9, 8, 5,
        [(1, 2, 9, 1),
         (1, 3, 11, 0),
         (2, 4, 1, 0),
         (2, 5, 6, 0),
         (5, 6, 9, 1),
         (5, 7, 4, 0),
         (6, 8, 3, 0),
         (6, 9, 1, 0)],
        [3, 4, 7, 8, 9]
    ))

    dummy.append(Test(
        4, 4, 3,
        [(1, 2, 2, 1),
         (2, 3, 10, 0),
         (1, 4, 3, 0),
         (4, 3, 4, 0)],
        [2, 3, 4]
    ))

    dummy.append(Test(
        6, 7, 4,
        [(1, 2, 15, 0),
         (1, 4, 1, 0),
         (4, 5, 1, 1),
         (5, 2, 13, 0),
         (2, 3, 2, 0),
         (3, 6, 4, 1),
         (5, 6, 3, 1)],
        [2, 5, 6, 3]
    ))

    for i, test in enumerate(dummy):
        test.validate()
        print>>sys.stderr, 'Generating test/%s.dummy.in.%d' % (PROBLEM, i+1)
        test.write(file('test/%s.dummy.in.%d' % (PROBLEM, i+1), 'wt'))

    subtask1, subtask2, subtask3, subtask4 = [], [], [], []

    # Subtask 1 -- M = N - 1,
    print("Generating Subtask1")
    for i in range(8):
        subtask1.append(gen_rand(100, 99, 99, 1, 1))

    for i in range(8):
        subtask1.append(gen_rand(5000, 4999, 4999, 1, 1))

    for i in range(8):
        subtask1.append(gen_rand(100000, 99999, 99999, 1, 1))

    # Subtask 2 -- K <= 100, samo jedan xi = 1
    print("Generating Subtask2")
    for i in range(8):
        subtask2.append(gen_rand(100, 100 * (i + 1), 30, 1, 1000))

    for i in range(8):
        subtask2.append(gen_rand(5000, 5000 * (i + 1), 30, 1, 100))

    for i in range(8):
        subtask2.append(gen_rand(100000, min(500000, 100000 * (i + 1)), 30, 1, 10**9))

    # Subtask 3 -- K <= 100
    print("Generating Subtask3")
    for i in range(8):
        subtask3.append(gen_rand(100, 100 * (i + 1), 30, 10 * (i + 1), 1000))

    for i in range(8):
        subtask3.append(gen_rand(5000, 5000 * (i + 1), 30, 10 * (i + 1), 100))

    for i in range(8):
        subtask3.append(gen_rand(100000, min(500000, 100000 * (i + 1)), 30, 10 * (i + 1), 10**9))

    # Subtask 4 -- nema ogranicenja
    # print("Generating Subtask4")
    print("Generating Subtask4")
    for i in range(8):
        subtask4.append(gen_rand(100, 100 * (i + 1), 99, 10 * (i + 1), 1000))

    for i in range(8):
        subtask4.append(gen_rand(5000, 5000 * (i + 1), 4999, 10 * (i + 1), 100))

    for i in range(8):
        subtask4.append(gen_rand(100000, min(500000, 100000 * (i + 1)), 99999, 10 * (i + 1), 10**9))

    for subtask in [subtask1, subtask2, subtask3, subtask4]:
        real.append(subtask)

    for i, batch in enumerate(real):
        for j, test in enumerate(batch):
            test.validate()
            print>>sys.stderr, 'Generating test/%s.in.%d%c' \
                % (PROBLEM, i+1, chr(ord('a')+j))
            input = 'test/%s.in.%d%c' % (PROBLEM, i+1, chr(ord('a')+j))
            test.write(file(input, 'wt'))


def main():
    random.seed(293487)
    gen_cases()


if __name__ == "__main__":
    main()
