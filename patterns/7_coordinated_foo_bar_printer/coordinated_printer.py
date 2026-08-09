from threading import Semaphore

# Very similar to problem 6 but with 2 systems
# so we could use semaphores to solve this problem (along with
# the condition variable strategies used in problem 6)

# Think of this problem as the bounded buffer problem (producer-consumer)
# with just one slot in the buffer where
# a producer putting an item in the buffer     <=> printing "Foo"
# a consumer consuming an item from the buffer <=> printing "Bar"
# Now it is the OSTEP textbook solution of the producer consumer problem
# with one buffer slot using semaphores and we don't need any locks here
# as there isn't any state we are updating which means no critical sections
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