from threading import Thread
from coordinated_printer import CoordinatedPrinter
from time import sleep

# Very similar to problem 6 but with 2 systems

def foo_worker(processor: CoordinatedPrinter):
    processor.printFoo()

def bar_worker(processor: CoordinatedPrinter):
    sleep(2)
    processor.printBar()

def main():
    processor = CoordinatedPrinter(10)

    foo_thread = Thread(target=foo_worker, args=(processor,))
    bar_thread = Thread(target=bar_worker, args=(processor,))
    foo_thread.start()
    bar_thread.start()
    foo_thread.join()
    bar_thread.join()

    print("All rounds finished!")

if __name__ == "__main__":
    main()
