import threading
import time

def print_numbers(name, count):
    for i in range(count):
        print(f"{name}: {i}")
        time.sleep(1)

def main():
    threads = []
    
    for i in range(3):
        # pass args with the args argument
        thread = threading.Thread(target=print_numbers, args=[f"thread-{i+1}", 5])
        threads.append(thread)
        thread.start()  

    # this would make the main thread wait for the thread to finish
    for thread in threads:
        thread.join()
    print("Main thread finished")

if __name__ == "__main__":
    main()

# Why must we separate the .start() loop from the .join() loop? 
# What would happen if we put .join() inside the first loop right after .start()?