from multiprocessing import Pool
import math
import cProfile
import io
import pstats

def f(x):
    return math.sqrt(1 - x**2)

def worker(i, delta_x):
    return f(i * delta_x) * delta_x

def approximate_pi_parallel(N):
    delta_x = 1.0 / N
    with Pool() as pool:
        result = pool.starmap(worker, [(i, delta_x) for i in range(N)])
    return 4 * sum(result)

def main():
    N = 1000000  # Number of rectangles
    pi_approx_parallel = approximate_pi_parallel(N)
    print(f"Approximate value of pi (parallel): {pi_approx_parallel}")

if __name__ == '__main__':
    profiler = cProfile.Profile()
    profiler.runcall(main)
    s = io.StringIO()
    ps = pstats.Stats(profiler, stream=s).sort_stats('time')
    ps.print_stats()
    print(s.getvalue())
