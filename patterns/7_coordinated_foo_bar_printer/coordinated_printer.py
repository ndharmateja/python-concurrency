from threading import Semaphore

# Very similar to problem 6 but with 2 systems
# so we could use semaphores to solve this problem
class CoordinatedPrinter:
    def __init__(self, n):
        self.n = n
        self.foo_sem = Semaphore(1)
        self.bar_sem = Semaphore(0)

    def printFoo(self):
        for _ in range(self.n):
            self.foo_sem.acquire()
            print("Foo")
            self.bar_sem.release()

    def printBar(self):
        for _ in range(self.n):
            self.bar_sem.acquire()
            print("Bar")
            self.foo_sem.release()