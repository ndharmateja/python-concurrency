import threading
import time

def print_message():
    for i in range(5):
        print("Hello from the thread!")
        time.sleep(1)

def main():
    thread = threading.Thread(target=print_message)
    thread.start()

    # this would make the main thread wait for the thread to finish
    thread.join()
    print("Main thread finished")

if __name__ == "__main__":
    main()

# What state is the main thread in while waiting on thread.join()? 
# Is it burning CPU cycles?
# Blocked => no CPU cycles wasted
# and GIL is also released so that the child thread could run