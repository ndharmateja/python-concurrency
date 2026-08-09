### Problem 1: Bounded Blocking Queue

Design and implement a thread-safe FIFO queue with a fixed capacity that supports concurrent producers and consumers without busy-waiting.

* **Interface:**
* `enqueue(item)`: Adds an item to the back of the queue.
* `dequeue()`: Removes and returns the item at the front of the queue.


* **Requirements & Invariants:**
1. **Capacity Limit:** If the queue is full (`size == capacity`), any thread calling `enqueue()` must block until space becomes available.
2. **Empty State:** If the queue is empty (`size == 0`), any thread calling `dequeue()` must block until an item is inserted.
3. **No Busy-Waiting:** Waiting threads must be put to sleep by the OS (using condition variables or semaphores) and woken up only when the queue state changes.
4. **Multi-Thread Safety:** Must support multiple concurrent producer and consumer threads without data races, lost updates, or corrupted pointers.



---

### Problem 2: Reader-Writer Lock (Writer-Preference)

Implement a custom synchronization lock that allows multiple concurrent readers or a single exclusive writer, explicitly configured to prevent writer starvation.

* **Interface:**
* `acquire_read()` / `release_read()`
* `acquire_write()` / `release_write()`


* **Requirements & Invariants:**
1. **Shared Reads:** Multiple reader threads can hold the lock simultaneously as long as no writer holds or is waiting for the lock.
2. **Exclusive Writes:** Only one writer thread can hold the lock at a time. No readers can hold the lock while a writer is active.
3. **Writer-Preference Invariant:** If a writer is waiting to acquire the lock, all newly arriving reader threads **must block** behind the waiting writer (even if other readers currently hold the lock). This guarantees that a steady stream of incoming readers cannot starve waiting writers indefinitely.



---

### Problem 3: Reusable Barrier

Design a synchronization primitive that blocks a fixed set of $N$ threads until all $N$ threads have reached a specific execution point, then releases them all and automatically resets for the next phase.

* **Interface:**
* `wait()`: Called by a thread to register its arrival at the barrier.


* **Requirements & Invariants:**
1. **Phase Gate:** Initialized with thread count $N$. The first $N-1$ threads to call `wait()` must put themselves to sleep.
2. **Simultaneous Release:** When the $N$-th thread calls `wait()`, all $N$ blocked threads must be unblocked to proceed.
3. **Reusability (Two-Phase Gate):** The barrier must immediately reset so that the exact same threads can call `wait()` again in a loop (e.g., in multi-step parallel matrix processing).
4. **No Race Conditions:** Fast threads returning for step 2 must not pass through the barrier before slow threads from step 1 have completely exited the barrier.



---

### Problem 4: Token Bucket Rate Limiter

Implement a thread-safe rate limiter based on the Token Bucket algorithm to control execution throughput across concurrent threads.

* **Interface:**
* `acquire(tokens=1)`: Requests a specified number of permits/tokens before allowing execution to proceed.


* **Requirements & Invariants:**
1. **Bucket Parameters:** Initialized with `capacity` (maximum tokens the bucket can hold) and `refill_rate` (number of tokens added per second).
2. **Token Consumption:** When `acquire(k)` is called:
* If at least $k$ tokens are in the bucket, consume $k$ tokens and return immediately.
* If fewer than $k$ tokens are present, block the calling thread until enough tokens have accumulated.


3. **No Background Worker Thread:** Token replenishment should be calculated dynamically on-demand using timestamp deltas (`current_time - last_refill_time`) rather than relying on a continuous, dedicated background timer thread.
4. **Thread Safety:** Multiple threads requesting tokens simultaneously must accurately decrement state without race conditions or negative token balances.



---

### Problem 5: Dining Philosophers (Resource Hierarchy)

Solve the classical Dining Philosophers synchronization problem for $N$ philosophers sitting around a circular table with $N$ forks, enforcing deadlock avoidance using a total order on resource acquisition.

* **Setup:**
* $N$ philosophers (threads) alternate between thinking and eating.
* $N$ forks (locks) are placed between them. Philosopher $i$ needs both fork $i$ (left) and fork $(i + 1) \pmod N$ (right) to eat.


* **Requirements & Invariants:**
1. **Mutual Exclusion:** No two adjacent philosophers can eat at the same time.
2. **Deadlock Freedom (Resource Hierarchy):** You must prevent circular wait deadlocks (where every philosopher picks up their left fork at the exact same time and waits forever for their right fork) by enforcing a global ordering rule: **threads must always acquire lower-indexed forks before higher-indexed forks**.
3. **Starvation Freedom:** No individual philosopher should be blocked indefinitely while adjacent neighbors repeatedly eat.



---

### Problem 6: Multi-Subsystem Ordered Log Processor

Synchronize three independent worker threads representing different subsystems ($A$, $B$, and $C$) to output their respective logs in a strict, deterministic round-robin order ($A \rightarrow B \rightarrow C \rightarrow A \dots$) for $K$ iterations.

#### Interface

* Thread 1 runs `print_first(log_a)` to process Subsystem $A$.
* Thread 2 runs `print_second(log_b)` to process Subsystem $B$.
* Thread 3 runs `print_third(log_c)` to process Subsystem $C$.

#### Requirements & Invariants

1. **Strict Ordering:** Output logs must follow the sequence $A \rightarrow B \rightarrow C \rightarrow A \dots$ without out-of-order interleaving.
2. **Spurious Wakeup Prevention:** Waiting threads must re-verify their turn condition inside a predicate loop (Mesa semantics).
3. **Targeted Signaling:** Avoid global broadcasts (`notify_all()`) if using Condition Variables to prevent unnecessary thread context switches and waking threads that cannot make progress.
4. **Clean Termination:** All three worker threads must complete $K$ rounds without leaving un-signaled waiting threads.



---

### Problem 7: Thread Coordinated Printing (Print FooBar Alternately)

Synchronize two independent threads so that they execute two distinct print functions in a strict, alternating sequence $N$ times.

* **Interface:**
* Thread 1 runs `foo(print_foo)` where `print_foo` outputs `"Foo"`.
* Thread 2 runs `bar(print_bar)` where `print_bar` outputs `"Bar"`.


* **Requirements & Invariants:**
1. **Strict Alternation:** The output across both threads must strictly form `"FooBarFooBarFooBar..."` repeated $N$ times.
2. **Scheduler Independence:** The synchronization logic must be completely independent of OS thread scheduling order. Even if Thread 2 (`bar`) starts running long before Thread 1 (`foo`), Thread 2 must wait until Thread 1 prints `"Foo"` first.
3. **Clean Termination:** Both threads must terminate cleanly after $N$ complete iterations without leaving lingering locks, un-handled waits, or race conditions.