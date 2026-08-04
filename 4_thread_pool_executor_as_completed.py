import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Thread
from utils import fn, print_countdown, print_duration

# 5 threads with thread pool executor
print()
print("5 threads with thread pool executor")

t = Thread(target=print_countdown, args=[8], daemon=True)
t.start()

start = time.perf_counter_ns()
with ThreadPoolExecutor() as executor:
    durations = [3, 6, 5, 8, 4]
    results = [ executor.submit(fn, s) for s in durations ]
    for completed_future in as_completed(results):
        print(completed_future.result())
finish = time.perf_counter_ns()
print_duration(start, finish)