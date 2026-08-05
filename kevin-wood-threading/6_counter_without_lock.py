import threading
import time

counter = 0

def increment(by):
    global counter
    for _ in range(by):
        temp = counter
        time.sleep(0)
        counter = temp + 1

def main():
    global counter
    by = 1000000
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

# Why does time.sleep(0) guarantee a heavily corrupted result, 
# and what Python bytecode instructions occur between 
# reading counter and writing to it?