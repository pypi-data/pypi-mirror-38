#! /home/maljovec/anaconda3/bin/python
import numpy as np
import sklearn.neighbors
import time
import numba
import argparse
import sys

parser = argparse.ArgumentParser(
    description="Build a Morse Complex using numba."
)
parser.add_argument(
    "-i",
    dest="p_file",
    type=str,
    required=True,
    help="The input data file as a csv.",
)
parser.add_argument(
    "-g", dest="g_file", type=str, required=True, help="The input graph file."
)
parser.add_argument(
    "-d",
    dest="d_file",
    type=str,
    required=True,
    help="The input distance file.",
)

args = parser.parse_args()

start = time.time()
X = np.load(args.p_file)
problem_size = X.shape[0]
dimensionality = X.shape[1]

end = time.time()
print("Load data ({} s) shape={}".format(end - start, X.shape), file=sys.stderr)
start = time.time()

edges = np.load(args.g_file)
distances = np.load(args.d_file)

end = time.time()
print(
    "Load graph ({} s) shape={}".format(end - start, edges.shape),
    file=sys.stderr,
)
start = time.time()


@numba.njit()
def gradient(Y, flow, edges, distances):
    for i in numba.prange(len(Y)):
        flow[i] = i
        max_value = 0
        for j, d in zip(edges[i], distances[i]):
            if j == -1:
                continue

            grad = (Y[j] - Y[i]) / d
            if grad > max_value:
                max_value = grad
                flow[i] = j


@numba.njit()
def local_maximum(flow, reps):
    last_count = 0
    count = len(np.unique(reps))
    while count != last_count:
        last_count = count
        for i in numba.prange(len(reps)):
            reps[i] = flow[i]
        count = len(np.unique(reps))


@numba.njit()
def determine_borders(reps, edges, border):
    for i in numba.prange(len(reps)):
        A = reps[i]
        for j in edges[i]:
            B = reps[j]
            if A != B:
                border[B, A] = border[A, B] = True


@numba.njit()
def saddle(Y, reps, edges, A, B):
    saddle_index = -1
    saddle_value = Y[A]
    for i in numba.prange(len(reps)):
        if i in [A, B] or reps[i] not in [A, B]:
            continue

        other_extremum = B if reps[i] == A else B

        for j in edges[i]:
            if j in [A, B] or reps[j] != other_extremum:
                continue

            if saddle_value > Y[i]:
                saddle_value = Y[i]
                saddle_index = i

            if saddle_value > Y[j]:
                saddle_value = Y[j]
                saddle_index = j

    return saddle_index


def persistence_hierarchy(saddles):
    pass
