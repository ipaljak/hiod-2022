#!/usr/bin/python3
"""Upotreba ./validate3.py test/*.in*"""

import hashlib
import glob
import string
import sys

sys.setrecursionlimit(10**6)


def dfs(node, dad, G):
    ret = 1
    for nxt in G[node]:
        if nxt == dad:
            continue
        ret += dfs(nxt, node, G)
    return ret


def check(lines):
    nl = []   # ispravno formatirane linije
    E = "\n"  # line ending

    n = int(lines[0].strip())
    assert 2 <= n <= 10**5, "n kriv"
    nl.append("{}{}".format(n, E))

    v = []
    edges = []
    for i in range(n):
        v.append([])
    for i in range(n - 1):
        a, b = map(int, lines[i + 1].split())
        assert a != b, "a = b"
        assert 1 <= a <= n, "a kriv"
        assert 1 <= b <= n, "b kriv"
        nl.append("{} {}{}".format(a, b, E))
        a -= 1
        b -= 1
        v[a].append(b)
        v[b].append(a)
        edges.append((min(a, b), max(a, b)))

    chain = True
    for i in range(n - 1):
        chain &= edges[i] == (i, i + 1)

    assert dfs(0, -1, v) == n, "nije stablo"

    assert lines == nl, "Krivi format (%s vs %s)" % (lines, nl)
    assert lines[-1][-1] == "\n", "Zadnji red ne zavrsava sa \\n"
    return {'n': n, 'chain': chain}


# Ocekivani clusteri! Ovo vjerojatno zelis promijeniti!
expected_clusters = {'s1': 1, 's2': 1, 's3': 1}


def what_cluster(data):
    # na temelju povratne informacije iz check(lines)
    # zakljucuje za TP u kojoj je bodovnoj sekciji
    if data['n'] <= 5000:
        return 's2'
    if data['chain']:
        return 's1'
    return 's3'


################### Zadatak-specifican kod iznad ove linije #########################


def group_in_batches(files):
    # mnozenje.in.1a, mnozenje.in.1b sprema u isti batch

    files.sort()
    B = []
    for f in files:
        if f[-1].islower() and len(B) > 0 and f[:-1] == B[-1][-1][:-1]:
            B[-1].append(f)
        else:
            B.append([f])
    return B


if __name__ == "__main__":
    f = []
    for pattern in sys.argv[1:]:
        for filename in glob.glob(pattern):
            f.append(filename)

    bc = []
    for batch in group_in_batches(f):
        if 'dummy' not in batch[0]:
            bc.append([])
        for filename in batch:
            print("{}: ".format(filename), end="")
            try:
                lines = open(filename).readlines()
                summary = check(lines)
                c = what_cluster(summary)
                if 'dummy' not in batch[0]:
                    bc[-1].append(c)
            except Exception as e:
                print("Greska!", e)
                raise
            else:
                print("Sve ok! (cluster {}, summary = {})".format(c, summary))

    print("RUCNO PROVJERI PRIPADNOST CLUSTERU")

    # clusters = {}
    # for b in bc:
        # # for c in b:
            # # assert c == b[0], "Ima razlicitih cluster-a unutar batcha"
        # if not b[0] in clusters:
            # clusters[b[0]] = 0
        # clusters[b[0]] += 1

    # assert clusters == expected_clusters, "Kriva raspodjela clustera ({} vs {})".format(
        # clusters, expected_clusters)

    # Buda test - provjeri duplikate
    # hashes = set(hashlib.sha1(open(x, 'rb').read()).hexdigest() for x in f)
    # assert len(hashes) == len(f), "Ima duplikata!"
