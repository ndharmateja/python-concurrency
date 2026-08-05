import threading
import time

def infinite_task():
    while True:
        print("Infinite task running...")
        time.sleep(1)

def main(): 
    daemon_thread = threading.Thread(target=infinite_task)
    daemon_thread.daemon = True
    daemon_thread.start()
    time.sleep(5)
    print("Main thread finished")

if __name__ == "__main__":
    main()

# If infinite_task had a try...finally block that closed 
# a database connection or flushed a file, would the finally block execute 
# when the main thread finishes?
# No, finally won't execute - as immediate process teardown happens