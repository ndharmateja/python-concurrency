from time import sleep
from random import uniform
from threading import Semaphore
from concurrent.futures import ThreadPoolExecutor

NUM_PHILOSOPHERS = 5
semaphores = [ Semaphore(1) for _ in range(NUM_PHILOSOPHERS) ]

def left_fork(philosopher_id) -> int : return philosopher_id
def right_fork(philosopher_id) -> int : return (philosopher_id + 1) % NUM_PHILOSOPHERS

def think(philosopher_id):
    print(f"Philosopher {philosopher_id} started thinking")
    sleep(uniform(0, 2))
    print(f"Philosopher {philosopher_id} finished thinking")

def eat(philosopher_id):
    print(f"Philosopher {philosopher_id} started eating")
    sleep(uniform(0, 2))
    print(f"Philosopher {philosopher_id} finished eating")

def get_forks(philosopher_id):
    if philosopher_id == NUM_PHILOSOPHERS - 1:
        semaphores[right_fork(philosopher_id)].acquire()
        print(f"Philosopher {philosopher_id} acquired right fork {right_fork(philosopher_id)}")
        semaphores[left_fork(philosopher_id)].acquire()
        print(f"Philosopher {philosopher_id} acquired left fork {left_fork(philosopher_id)}")
    else:
        semaphores[left_fork(philosopher_id)].acquire()
        print(f"Philosopher {philosopher_id} acquired left fork {left_fork(philosopher_id)}")
        semaphores[right_fork(philosopher_id)].acquire()
        print(f"Philosopher {philosopher_id} acquired right fork {right_fork(philosopher_id)}")

def put_forks(philosopher_id):
    semaphores[left_fork(philosopher_id)].release()
    print(f"Philosopher {philosopher_id} released left fork {left_fork(philosopher_id)}")
    semaphores[right_fork(philosopher_id)].release()
    print(f"Philosopher {philosopher_id} released right fork {right_fork(philosopher_id)}")

def worker(philosopher_id):
    # Say each philosopher wants to think and eat for 3 times
    for _ in range(3):
        think(philosopher_id)
        get_forks(philosopher_id)
        eat(philosopher_id)
        put_forks(philosopher_id)

def main():
    with ThreadPoolExecutor() as executor:
        futures = [ executor.submit(worker, i) for i in range(NUM_PHILOSOPHERS) ]
        for f in futures:
            f.result()

if __name__ == "__main__":
    main()