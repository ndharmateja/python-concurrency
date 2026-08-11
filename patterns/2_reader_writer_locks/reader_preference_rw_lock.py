from threading import Semaphore

class ReaderPreferencRWLock:
    def __init__(self):
        self.mutex = Semaphore(1)
        self.write_lock = Semaphore(1)
        self.num_readers = 0

    def acquire_read_lock(self):
        with self.mutex:
            # The first reader gets hold of the write lock (locks
            # out writers)
            self.num_readers += 1
            if self.num_readers == 1:
                self.write_lock.acquire()
    
    def release_read_lock(self):
        with self.mutex:
            # The last reader lets go of the write lock (lets in writers
            # if there are any)
            self.num_readers -= 1
            if self.num_readers == 0:
                self.write_lock.release()

    def acquire_write_lock(self):
        self.write_lock.acquire()

    def release_write_lock(self):
        self.write_lock.release()
