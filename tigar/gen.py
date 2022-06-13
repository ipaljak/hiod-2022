#!/usr/bin/python2

import subprocess
import random
import os
import glob
import sys
doc = """
  Cenerate all test cases in test/:  gen.py
"""


PROBLEM = "tigar"
sys.setrecursionlimit(1000010)

MAXN = 100000


class Test(object):
    def __init__(self, n, e):
        self.n = n  # number of vertices
        self.e = e  # list of edges [(1, 2), (4, 5), ...]

    def validate(self):
        assert(2 <= self.n <= MAXN)
        assert(len(self.e) == self.n - 1)
        adj = [[] for x in range(0, self.n + 1)]
        for a, b in self.e:
            assert(1 <= a and a <= self.n)
            assert(1 <= b and b <= self.n)
            assert(a != b)
            adj[a].append(b)
            adj[b].append(a)

        bio = {}

        def dfs(x, dad):
            bio[x] = True
            for y in adj[x]:
                if y == dad:
                    continue
                assert(y not in bio)
                dfs(y, x)
        dfs(1, -1)
        for x in range(1, self.n + 1):
            assert(x in bio)

    def write(self, fd=sys.stdout):
        print>>fd, self.n
        for a, b in self.e:
            print>>fd, a, b


def remove_cases():
    cases = glob.glob('test/%s.dummy.in.*' % PROBLEM)
    cases += glob.glob('test/%s.dummy.out.*' % PROBLEM)
    cases += glob.glob('test/%s.in.*' % PROBLEM)
    cases += glob.glob('test/%s.out.*' % PROBLEM)
    for c in cases:
        print>>sys.stderr, 'Removing ' + c
        os.remove(c)

# generiraj random string, p vjerojatnost da bude otvorena zagrada


def paren_random(n, e, p):
    return ''.join(['(' if random.randint(1, 100) <= p else ')' for x in range(n)])

# u svakoj iteraciji uzmi random cvor i pusti dfs koji popunjava zagrade sa pozitivnim balansom


def paren1(n, e, p):
    z = ['(' if random.randint(0, 1) == 0 else ')' for x in range(n)]
    adj = {}
    for x in xrange(1, n + 1):
        adj[x] = []
    for a, b in e:
        adj[a].append(b)
        adj[b].append(a)

    def dfs(x, dad, bal):
        if (random.randint(0, 100) == 0):
            return
        if (bal == 0):
            z[x-1] = '('
        else:
            z[x-1] = '(' if random.randint(0, 1) == 0 else ')'

        bal += (1 if z[x-1] == '(' else -1)

        for y in adj[x]:
            if y != dad:
                dfs(y, x, bal)

    for it in range(100):
        x = random.randint(1, n)
        dfs(x, -1, 0)

    return ''.join(z)


def gen_random(n):
    e = [(x, random.randint(1, x - 1)) for x in range(2, n + 1)]
    return Test(n, e)


def gen_deep(n, sw):
    e = [(x, random.randint(max(1, x - sw), x - 1)) for x in range(2, n + 1)]
    return Test(n, e)


def gen_star(n):
    e = [(x, 1) for x in range(2, n + 1)]
    return Test(n, e)


def gen_chain(n):
    return gen_deep(n, 1)



def gen_test3(n):
    e = [(x, 1) if x <= n/2 else (x, 2) for x in range(2, n + 1)]
    return Test(n, e)


def gen_cases():
    remove_cases()

    real = []
    dummy = []

    dummy.append(Test(
        5,
        [(1, 2), (2, 3), (3, 4), (4, 5)]
    ))

    dummy.append(Test(
        10,
        [(1, 2), (2, 4), (5, 2), (6, 3), (3, 1), (6, 7), (9, 7), (8, 6), (8, 10)]
    ))

    dummy.append(Test(
        6,
        [(3, 1), (3, 5), (4, 3), (4, 2), (2, 6)]
    ))

    for i, test in enumerate(dummy):
        test.validate()
        print>>sys.stderr, 'Generating test/%s.dummy.in.%d' % (PROBLEM, i+1)
        test.write(file('test/%s.dummy.in.%d' % (PROBLEM, i+1), 'wt'))

    # subtask 1 -- 1 <= n <= 300
    subtask1 = []
    for i in range(1, 7):
        print('Generating subtask 1, case ', i)
        subtask1.append(gen_random(random.randint(10, 15)))

    for i in range(7, 16):
        print('Generating subtask 1, case ', i)
        subtask1.append(gen_random(random.randint(10, 15)))

    print('Generating subtask 1, case 16')

    subtask1.append(Test(
        15,
        [(2, 1),
         (3, 1),
         (4, 2),
         (5, 2),
         (6, 5),
         (7, 6),
         (8, 1),
         (9, 2),
         (10, 1),
         (11, 10),
         (12, 8),
         (13, 8),
         (14, 11),
         (15, 3)]))

    print('Generating subtask 1, case 17')
    subtask1.append(Test(
        15,
        [(2, 1),
         (3, 1),
         (4, 2),
         (5, 1),
         (6, 3),
         (7, 6),
         (8, 5),
         (9, 4),
         (10, 5),
         (11, 6),
         (12, 1),
         (13, 8),
         (14, 2),
         (15, 1)]))

    print('Generating subtask 1, case 18')
    subtask1.append(Test(
        15,
        [(2, 1),
         (3, 2),
         (4, 2),
         (5, 3),
         (6, 4),
         (7, 6),
         (8, 7),
         (9, 4),
         (10, 2),
         (11, 3),
         (12, 8),
         (13, 11),
         (14, 8),
         (15, 12)]))

    print('Generating subtask 1, case 19')
    subtask1.append(Test(
        15,
        [(2, 1),
         (3, 1),
         (4, 1),
         (5, 2),
         (6, 1),
         (7, 1),
         (8, 4),
         (9, 8),
         (10, 4),
         (11, 1),
         (12, 7),
         (13, 7),
         (14, 2),
         (15, 5)]))

    print('Generating subtask 1, case 20')
    subtask1.append(gen_random(2))

    print('Generating subtask 1, case 21')
    subtask1.append(gen_random(15))

    for i in range(1, 6):
        print('Generating subtask 1, case ', i)
        subtask1.append(gen_deep(1000, 5*i))

    for i in range(6, 11):
        print('Generating subtask 1, case ', i)
        subtask1.append(gen_random(1000))

    for i in range(11, 14):
        print('Generating subtask 1, case ', i)
        subtask1.append(gen_random(1000))

    for i in range(14, 17):
        print('Generating subtask 1, case ', i)
        subtask1.append(gen_random(1000))

    real.append(subtask1)

    # subtask 2, 1 <= n <= 5000
    subtask2 = []
    for i in range(1, 6):
        print('Generating subtask 2, case ', i)
        subtask2.append(gen_deep(5000, 5*i))

    for i in range(6, 11):
        print('Generating subtask 2, case ', i)
        subtask2.append(gen_random(5000))

    for i in range(11, 14):
        print('Generating subtask 2, case ', i)
        subtask2.append(gen_random(5000))

    for i in range(14, 17):
        print('Generating subtask 2, case ', i)
        subtask2.append(gen_random(5000))

    print('Generating subtask 2, case 17')
    subtask2.append(gen_star(5000))

    real.append(subtask2)

    # subtask 3, 1 <= n <= 100 000
    subtask3 = []
    for i in range(1, 5):
        print('Generating subtask 3, case ', i)
        subtask3.append(gen_deep(MAXN, 5*i))

    for i in range(5, 7):
        print('Generating subtask 3, case ', i)
        subtask3.append(gen_random(MAXN))

    for i in range(7, 9):
        print('Generating subtask 3, case ', i)
        subtask3.append(gen_random(MAXN))

    for i in range(9, 11):
        print('Generating subtask 3, case ', i)
        subtask3.append(gen_random(MAXN))

    print('Generating subtask 3, case 11')
    subtask3.append(gen_star(MAXN))
    real.append(subtask3)

    for i, batch in enumerate(real):
        for j, test in enumerate(batch):
            test.validate()
            print>>sys.stderr, 'Generating test/%s.in.%d%c%c' % (
                PROBLEM, i+1, chr(ord('a')+(j/26)), chr(ord('a') + (j % 26)))
            input = 'test/%s.in.%d%c%c' % (PROBLEM, i+1, chr(ord('a')+(j/26)), chr(ord('a') + (j % 26)))
            test.write(file(input, 'wt'))


def main():
    random.seed(293487)
    gen_cases()


if __name__ == "__main__":
    main()
