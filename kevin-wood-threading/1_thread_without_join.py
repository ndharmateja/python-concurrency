import threading
import time

def print_message():
    for i in range(5):
        print("Hello from the thread!")
        time.sleep(1)

def main():
    thread = threading.Thread(target=print_message)
    thread.start()
    print("Main thread finished")

if __name__ == "__main__":
    main()

# Why does 'Main thread finished' print almost immediately while 
# 'Hello from the thread!' keeps printing for 5 seconds?