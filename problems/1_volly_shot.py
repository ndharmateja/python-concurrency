from concurrent.futures import ThreadPoolExecutor, as_completed
import time

def vollyShot(indices, shot_func, max_workers: int = 50) -> bool:
    # Bounded ThreadPoolExecutor prevents OS resource exhaustion
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks and keep a mapping of Future -> index
        future_to_index = {
            executor.submit(shot_func, idx): idx 
            for idx in indices
        }
        
        # as_completed yields futures as soon as they finish (in completion order)
        for future in as_completed(future_to_index):
            try:
                result = future.result()
                if result is True:
                    # EARLY EXIT: Short-circuit immediately!
                    # Cancel any pending futures in the queue that haven't started running yet
                    for f in future_to_index:
                        f.cancel()
                    return True
            except Exception:
                # If an individual API call fails/errors, ignore and continue checking others
                continue
                
    # If loop completes and no call returned True
    return False

# Interview Origin: 
# IMG_7016 (Execute shot(i) concurrently for up to 1,000 indices. 
# Return True immediately when any call succeeds. 
# Return False only if all fail).

# The Mental Model
# Creating 1,000 raw threads is inefficient (causes OS thread stack memory exhaustion).
# We use ThreadPoolExecutor to bound the workers (e.g., 50–100 workers for I/O tasks)
# and process results out-of-order as they finish using as_completed().

# Key Interview Probing Points to Teach Your Student:
# Worker Pool Sizing: For CPU-bound tasks, set max_workers = os.cpu_count(). 
# For I/O-bound blocking calls (like shot() taking 1–10s), set max_workers 
# significantly higher (e.g., 50 to 100) because threads spend most of their time 
# in WAITING state, releasing the GIL.

# Cancellation Mechanics: 
# Explain that future.cancel() only cancels tasks waiting in the queue. 
# It cannot interrupt a thread currently executing inside the shot() I/O block 
# unless the low-level socket supports timeouts/cancellation flags.