from time import sleep
from random import uniform
from concurrent.futures import ThreadPoolExecutor
from reusable_barrier_cv import ReusableBarrier

NUM_THREADS = 5

def worker(id, barrier):
    # First phase of the work before the barrier
    print(f"Begin thread {id}")
    sleep(uniform(id + 1, id + 3))

    # Wait for all the threads to arrive at the barrier
    print(f"thread {id} arrived at the first barrier")
    barrier.wait()
    print(f"thread {id} crossed the first barrier")

    # Second phase of work
    sleep(uniform((NUM_THREADS - id) + 3, (NUM_THREADS - id) + 5))

    # Wait for all the threads to arrive at the barrier again
    print(f"thread {id} arrived at the second barrier")
    barrier.wait()
    print(f"thread {id} crossed the second barrier and done")

def main():
    barrier = ReusableBarrier(NUM_THREADS)
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(worker, id, barrier) for id in range(NUM_THREADS)]
        for future in futures:
            future.result()

    print("Main thread done!")

if __name__ == "__main__":
    main()