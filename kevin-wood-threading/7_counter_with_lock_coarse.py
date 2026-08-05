import threading
import time

counter = 0
counter_lock = threading.Lock()

def increment(by):
    global counter

    # no chance of concurrency as we locked the entire loop
    # and the other threads have to wait until this thread
    # finishes
    with counter_lock:
        for _ in range(by):
            temp = counter
            time.sleep(0)
            counter = temp + 1

def main():
    global counter
    by = 5
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

# This code produces the correct result, but why does it defeat 
# the purpose of using multiple threads?