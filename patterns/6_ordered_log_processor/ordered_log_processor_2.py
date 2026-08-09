from threading import Lock, Condition

# Same as the first one except we use a different CV for each of the subsystems
# so that we don't have to notify_all() and just use notify() on the particular 
# subsystem.
# Each subsystem only waits on its CV.

class OrderedLogProcessor:
    def __init__(self):
        self.lock = Lock()
        self.first_cond = Condition(self.lock)
        self.second_cond = Condition(self.lock)
        self.third_cond = Condition(self.lock)

        # 0 = First subsystem's turn
        # 1 = Second subsystem's turn
        # 2 = Third subsystem's turn
        self.state = 0

    def printFirst(self, log):
        with self.lock:
            # Wait on the CV as long as it is not the first's turn
            while self.state != 0:
                self.first_cond.wait()
            
            # Execute work
            print(log)

            # It is second's turn next
            self.state = 1
            self.second_cond.notify()

    def printSecond(self, log):
        with self.lock:
            # Wait on the CV as long as it is not the second's turn
            while self.state != 1:
                self.second_cond.wait()
            
            # Execute work
            print(log)
            
            # It is third's turn next
            self.state = 2
            self.third_cond.notify()

    def printThird(self, log):
        with self.lock:
            # Wait on the CV as long as it is not the third's turn
            while self.state != 2:
                self.third_cond.wait()
            
            # Execute work
            print(log)
            
            # It is first's turn next
            self.state = 0 
            self.first_cond.notify()