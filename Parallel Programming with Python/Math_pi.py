import time
import math
import cProfile

def f(x):
    return math.sqrt(1 - x**2)

def approximate_pi(N):
    delta_x = 1.0 / N
    return 4 * sum(f(i * delta_x) * delta_x for i in range(N))

def main():
    N = 1000000  # Number of rectangles
    pi_approx = approximate_pi(N)
    print(f"Approximate value of pi: {pi_approx}")

# Profile
if __name__ == '__main__':
    profiler = cProfile.Profile()
    profiler.runcall(main)
    profiler.print_stats(sort='time')
