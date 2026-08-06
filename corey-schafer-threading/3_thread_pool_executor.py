import time
from concurrent.futures import ThreadPoolExecutor
from utils import print_duration, fn

# 2 threads with thread pool executor
print()
print("2 threads with thread pool executor")

start = time.perf_counter_ns()
with ThreadPoolExecutor() as executor:
    f1 = executor.submit(fn, 3)
    f2 = executor.submit(fn, 1)
    print(f1.result())
    print(f2.result())
finish = time.perf_counter_ns()
print_duration(start, finish)