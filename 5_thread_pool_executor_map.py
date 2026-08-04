import time
from concurrent.futures import ThreadPoolExecutor
from threading import Thread
from utils import fn, print_countdown, print_duration

# 5 threads with thread pool executor
print()
print("5 threads with thread pool executor")

t = Thread(target=print_countdown, args=[8], daemon=True)
t.start()

start = time.perf_counter_ns()
with ThreadPoolExecutor() as executor:
    # map would wait for all the threads to join
    # (even without the next for loop)
    durations = [3, 9, 6, 4]
    results = executor.map(fn, durations)

    # this will iterate in order of function beginnings
    for result in results:
        print(result)
    
finish = time.perf_counter_ns()
print_duration(start, finish)