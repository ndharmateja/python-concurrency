import threading
import time

counter = 0
counter_lock = threading.Lock()

def increment(by):
    global counter
    local_counter = 0
    for _ in range(by):
        local_counter += 1

    with counter_lock:
        counter += local_counter


def main():
    global counter
    by = 100_000_000
    num_threads = 3
    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=increment, args=[by])
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()

    print(f"Final counter value:")
    print(f"Expected: {num_threads * by}")
    print(f"Actual  : {counter}")

if __name__ == "__main__":
    main()

# How does this pattern eliminate lock contention while scaling to 
# billions of operations across hundreds of threads?