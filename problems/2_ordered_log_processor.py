import threading
import time
import random

class OrderedLogProcessor:
    def __init__(self):
        self.lock = threading.Lock()
        self.cond = threading.Condition(self.lock)
        # 0 = Subsystem A's turn, 1 = Subsystem B's turn, 2 = Subsystem C's turn
        self.state = 0

    def printFirst(self, print_a_func):
        with self.cond:
            # Mesa Semantics: Always re-check condition in a while loop
            while self.state != 0:
                self.cond.wait()
            
            # Execute work
            print_a_func()
            
            # Update state transition (0 -> 1)
            self.state = 1
            # Must notify_all because other waiting threads might be 'C' (who should stay asleep)
            self.cond.notify_all()

    def printSecond(self, print_b_func):
        with self.cond:
            while self.state != 1:
                self.cond.wait()
            
            print_b_func()
            
            self.state = 2
            self.cond.notify_all()

    def printThird(self, print_c_func):
        with self.cond:
            while self.state != 2:
                self.cond.wait()
            
            print_c_func()
            
            self.state = 0 # Loop back to A
            self.cond.notify_all()


def print_subsystem_a():
    print("[A]: Log line")

def print_subsystem_b():
    print("[B]: Log line")

def print_subsystem_c():
    print("[C]: Log line")


def worker_a(processor, iterations):
    for _ in range(iterations):
        time.sleep(random.uniform(0.1, 0.5))
        print("log line from A generated")
        processor.printFirst(print_subsystem_a)

def worker_b(processor, iterations):
    time.sleep(2)
    for _ in range(iterations):
        time.sleep(random.uniform(0.5, 1))
        print("log line from B generated")
        processor.printSecond(print_subsystem_b)

def worker_c(processor, iterations):
    for _ in range(iterations):
        time.sleep(random.uniform(1, 3))
        print("log line from C generated")
        processor.printThird(print_subsystem_c)


def main():
    processor = OrderedLogProcessor()
    rounds = 4 

    targets = [worker_c, worker_b, worker_a]
    threads = []

    for target in targets:
        thread = threading.Thread(target=target, args=(processor, rounds))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print("All rounds finished!")

if __name__ == "__main__":
    main()
