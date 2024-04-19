from mpi4py import MPI
import math
import numpy as np
import cProfile
import io
import pstats

def f(x):
    return math.sqrt(1 - x**2)

def compute_local_sum(local_a, local_n, delta_x):
    return np.sum([f(local_a + i * delta_x) * delta_x for i in range(local_n)])

def main():
    comm = MPI.COMM_WORLD
    size = comm.Get_size()
    rank = comm.Get_rank()

    if rank == 0:
        N = 1000000  # This can be changed to experiment with different values of N
    else:
        N = None
    N = comm.bcast(N, root=0)

    delta_x = 1.0 / N
    local_n = N // size
    local_a = rank * local_n * delta_x

    local_sum = compute_local_sum(local_a, local_n, delta_x)

    pi_val = comm.reduce(local_sum, op=MPI.SUM, root=0)

    if rank == 0:
        print(f"Approximate value of pi (distributed): {4 * pi_val}")

if __name__ == "__main__":
    pr = cProfile.Profile()
    pr.enable()
    main()
    pr.disable()
    s = io.StringIO()
    sortby = pstats.SortKey.CUMULATIVE
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats()
    print(s.getvalue())
