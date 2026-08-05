import threading
import time

counter = 0
counter_lock = threading.Lock()

def increment(by):
    global counter
    thread_name = threading.current_thread().name

    # extra overhead as we are locking and unlocking 
    # in every iteration
    for _ in range(by):
        with counter_lock:
            temp = counter
            counter = temp + 1
            print(f"thread-{thread_name} incremented counter to {counter}")
        time.sleep(0.1)

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

# Why is this script significantly slower than holding the lock 
# outside the loop, even though both yield the correct counter?