#!/usr/bin/python3
"""Upotreba ./validate3.py test/*.in*"""

import string


def check(lines):
    nl = []   # ispravno formatirane linije
    E = "\n"  # line ending

    n, k = map(int, lines[0].split())
    assert 1 <= n*k <= 2000000, "nk kriv"
    assert 1 <= n, "wtf n"
    assert 1 <= k, "wtf k"
    nl.append("{} {}{}".format(n, k, E))

    for i in range(n):
        a = list(map(int, lines[i + 1].split()))
        assert len(a) == k, "duljina a kriva"
        assert sorted(a) == list(range(1, k + 1)), "nije permutacija"
        nl.append("{}{}".format(' '.join(list(map(str, a))), E))

    assert lines == nl, "Krivi format (%s vs %s)" % (lines, nl)
    assert lines[-1][-1] == "\n", "Zadnji red ne zavrsava sa \\n"
    return {'n': n, 'k': k}


# Ocekivani clusteri! Ovo vjerojatno zelis promijeniti!
expected_clusters = {'s1': 1, 's2': 1, 's3': 1, 's4': 1, 's5': 1, 's6': 1, 's7': 1, 's8': 1}


def what_cluster(data):
    # na temelju povratne informacije iz check(lines)
    # zakljucuje za TP u kojoj je bodovnoj sekciji
    if data['n'] <= 10**5 and data['k'] == 1: return 's1'
    if data['n'] <= 5000 and data['k'] == 2: return 's2'
    if data['n'] <= 10**5 and data['k'] == 2: return 's3'
    if data['n'] <= 5000 and data['k'] <= 5: return 's4'
    if data['n'] <= 10**5 and data['k'] <= 5: return 's5'
    if data['n'] <= 5000 and data['k'] <= 20: return 's6'
    if data['n'] <= 10**5 and data['k'] <= 20: return 's7'
    return 's8'



################### Zadatak-specifican kod iznad ove linije #########################

import sys
import glob
import hashlib


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

    clusters = {}
    for b in bc:
        for c in b:
            assert c == b[0], "Ima razlicitih cluster-a unutar batcha"
        if not b[0] in clusters:
            clusters[b[0]] = 0
        clusters[b[0]] += 1

    assert clusters == expected_clusters, "Kriva raspodjela clustera ({} vs {})".format(clusters, expected_clusters)

    # Buda test - provjeri duplikate
    hashes = set(hashlib.sha1(open(x, 'rb').read()).hexdigest() for x in f)
    assert len(hashes) == len(f), "Ima duplikata!"
