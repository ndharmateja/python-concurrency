from threading import Semaphore

class WriterPreferencRWLock:
    def __init__(self):
        self.mutex = Semaphore(1)
        self.main_lock = Semaphore(1)
        self.writers_sem = Semaphore(1)
        self.active_readers = 0
        self.waiting_readers = 0
        self.active_writers = 0
        self.waiting_writers = 0
        pass

    def acquire_read_lock(self):
        # If there are no waiting/active writer threads we could directly let
        # the reader thread through
        # but if it is the first reader thread it should acquire the main lock
        # and writers semaphore first
        with self.mutex:
            if (self.active_writers == 0 and self.waiting_writers == 0):
                self.active_readers += 1
                if self.active_readers == 1:
                    self.writers_sem.acquire()
                    self.main_lock.acquire()
                return

        # Waiting case
        with self.mutex:
            self.waiting_readers += 1
        self.main_lock.acquire()

            
    
    def release_read_lock(self):
        with self.mutex:
            self.active_readers -= 1

            # If there are still active readers, we don't need to do anything
            if self.active_readers:
                return

        # If we reached here it means that there are no more active readers
        # and this is the last active reader releasing the read lock
        # If there are waiting writers, then we signal one of those
        # and the main lock is released by the writers after they are done
        # If there are no waiting writers, then we need to release the main lock
        with self.mutex:
            if self.waiting_writers:
                self.writers_sem.release()
            else:
                self.main_lock.release()


    def acquire_write_lock(self):
        # If active readers, wait for the readers to finish
        # If active writer/waiting writers, wait for a writer thread to 
        # be woken up
        with self.mutex:
            self.waiting_writers += 1

        # The main lock is passed from the last reader thread to the first
        # waiting writer thread
        # But if the writer thread was called first while there were no
        # reading threads, we also need to acquire the main lock
        with self.mutex:
            if self.active_readers == 0 and self.waiting_readers == 0 and self.active_writers == 0:
                self.main_lock.acquire()
        self.writers_sem.acquire()

        # At this point we are ready to acquire the lock for the writer
        # so the current writer moves from waiting to active
        with self.mutex:
            self.waiting_writers -= 1
            self.active_writers = 1

    def release_write_lock(self):
        # If there are waiting writers, then we signal one of them
        # We ensure this by releasing the writers_sem which would wake
        # up one of the waiting writer threads (we are not releasing
        # and reacquiring the main lock so that none of the waiting
        # reader threads are woke up)
        # The writer lock is passed from one writer to the next
        self.active_writers = 0
        self.writers_sem.release()

        # If there are no more waiting writers, then we can release the main lock
        # so that one of the waiting reader threads (if any) gets woken up
        if self.waiting_writers == 0:
            self.main_lock.release()
    