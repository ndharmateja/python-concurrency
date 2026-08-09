from threading import Thread
import time
import random
from ordered_log_processor_2 import OrderedLogProcessor

def worker_a(processor: OrderedLogProcessor, iterations):
    for _ in range(iterations):
        time.sleep(random.uniform(1, 3))
        print("log line from A generated")
        processor.print_first("[A] log line")

def worker_b(processor: OrderedLogProcessor, iterations):
    time.sleep(2)
    for _ in range(iterations):
        time.sleep(random.uniform(0.5, 1))
        print("log line from B generated")
        processor.print_second("[B] log line")

def worker_c(processor: OrderedLogProcessor, iterations):
    for _ in range(iterations):
        time.sleep(random.uniform(0.1, 0.5))
        print("log line from C generated")
        processor.print_third("[C] log line")


def main():
    processor = OrderedLogProcessor()
    rounds = 4 

    targets = [worker_c, worker_a, worker_b]
    threads = []

    for target in targets:
        thread = Thread(target=target, args=(processor, rounds))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print("All rounds finished!")

if __name__ == "__main__":
    main()
