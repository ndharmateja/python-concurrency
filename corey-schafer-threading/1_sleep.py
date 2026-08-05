import time
from threading import Thread
from utils import print_duration, fn

# Sequential (synchronous) execution
print("No threads")
start = time.perf_counter_ns()
fn()
fn()
finish = time.perf_counter_ns()
print_duration(start, finish)

# 2 threads
print()
print("With 2 threads")

start = time.perf_counter_ns()
t1 = Thread(target=fn)
t2 = Thread(target=fn)
t1.start()
t2.start()
t1.join()
t2.join()
finish = time.perf_counter_ns()
print_duration(start, finish)

# 10 threads
print()
print("With 10 threads")

start = time.perf_counter_ns()
threads = []
for _ in range(10):
    t = Thread(target=fn)
    threads.append(t)
    t.start()
for t in threads:
    t.join()
finish = time.perf_counter_ns()
print_duration(start, finish)
