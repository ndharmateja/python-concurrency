import threading
import time

def print_numbers(name, count):
    for i in range(count):
        print(f"{name}: {i}")
        time.sleep(1)

def main():
    # pass args with the args argument
    thread = threading.Thread(target=print_numbers, args=["thread", 5])
    thread.start()

    # this would make the main thread wait for the thread to finish
    thread.join()
    print("Main thread finished")

if __name__ == "__main__":
    main()

# What happens if you pass target=print_numbers("thread", 5) directly 
# instead of using the args parameter?