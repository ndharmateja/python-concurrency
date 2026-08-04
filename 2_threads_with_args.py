import time
from threading import Thread
from utils import print_duration, fn

# 5 threads sequentially
print()
print("With 5 threads sequentially")

start = time.perf_counter_ns()
threads = []
for i in range(1, 6):
    t = Thread(target=fn, args=[i])
    threads.append(t)
    t.start()
    t.join()
finish = time.perf_counter_ns()
print_duration(start, finish)

# 5 threads concurrently
print() 
print("With 5 threads concurrently")

start = time.perf_counter_ns()
threads = []
for i in range(1, 6):
    t = Thread(target=fn, args=[i])
    threads.append(t)
    t.start()
for t in threads:
    t.join()
finish = time.perf_counter_ns()
print_duration(start, finish)