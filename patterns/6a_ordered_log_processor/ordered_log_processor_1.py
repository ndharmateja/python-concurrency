from threading import Lock, Condition

class OrderedLogProcessor:
    def __init__(self):
        self.lock = Lock()
        self.cond = Condition(self.lock)

        # 0 = First subsystem's turn
        # 1 = Second subsystem's turn
        # 2 = Third subsystem's turn
        self.state = 0

    def printFirst(self, log):
        with self.lock:
            # Wait on the CV as long as it is not the first's turn
            while self.state != 0:
                self.cond.wait()
            
            # Execute work
            print(log)

            # It is second's turn next and we notify_all() as both the second and third
            # could be waiting and notify doesn't specify which one it would wake up
            self.state = 1
            self.cond.notify_all()

    def printSecond(self, log):
        with self.lock:
            # Wait on the CV as long as it is not the second's turn
            while self.state != 1:
                self.cond.wait()
            
            # Execute work
            print(log)
            
            # It is third's turn next and we notify_all() as both the first and third
            # could be waiting and notify doesn't specify which one it would wake up
            self.state = 2
            self.cond.notify_all()

    def printThird(self, log):
        with self.lock:
            # Wait on the CV as long as it is not the third's turn
            while self.state != 2:
                self.cond.wait()
            
            # Execute work
            print(log)
            
            # It is first's turn next and we notify_all() as both the first and second
            # could be waiting and notify doesn't specify which one it would wake up
            self.state = 0 
            self.cond.notify_all()