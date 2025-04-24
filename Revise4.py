import gc
import random
import psutil
import time
import matplotlib.pyplot as plt
import seaborn as sns
from collections import deque

# -----------------------------
# Configuration & Setup
# -----------------------------

sns.set(style="whitegrid", palette="coolwarm")
MAX_ITERATIONS = 5                # Number of monitoring cycles
OBJECT_COUNT = 10000              # Number of objects to allocate
LIST_SIZE = 100                   # Size of each allocated object (list)
memory_stats = deque(maxlen=MAX_ITERATIONS)  # Stores memory usage logs

# -----------------------------
# Helper Functions
# -----------------------------

def allocate_memory(num_objects=OBJECT_COUNT, list_size=LIST_SIZE):
    """
    Simulates memory allocation by creating a list of random float lists.
    """
    return [[random.random() for _ in range(list_size)] for _ in range(num_objects)]

def get_current_memory():
    """
    Returns the current process memory usage in megabytes.
    """
    process = psutil.Process()
    memory_bytes = process.memory_info().rss
    return memory_bytes / (1024 * 1024)  # Convert bytes to MB

def monitor_memory_usage():
    """
    Tracks memory usage:
    - Before allocation
    - After allocation
    - After garbage collection
    Appends the results to memory_stats.
    """
    mem_before = get_current_memory()
    data = allocate_memory()
    mem_after_alloc = get_current_memory()

    del data  # Free allocated memory
    gc.collect()  # Run garbage collector
    mem_after_gc = get_current_memory()

    memory_stats.append((mem_before, mem_after_alloc, mem_after_gc))

# -----------------------------
# Execution Loop
# -----------------------------

for _ in range(MAX_ITERATIONS):
    monitor_memory_usage()
    time.sleep(1)  # Short delay to simulate time between cycles

# -----------------------------
# Data Preparation for Plotting
# -----------------------------

iterations = list(range(1, MAX_ITERATIONS + 1))
mem_before = [record[0] for record in memory_stats]
mem_allocated = [record[1] for record in memory_stats]
mem_after_gc = [record[2] for record in memory_stats]

# -----------------------------
# Plotting
# -----------------------------

plt.figure(figsize=(10, 6))

plt.plot(iterations, mem_before, marker='o', linestyle='--', linewidth=2, label='Before Allocation')
plt.plot(iterations, mem_allocated, marker='s', linestyle=':', linewidth=2, label='After Allocation')
plt.plot(iterations, mem_after_gc, marker='^', linestyle='-', linewidth=2, label='After GC')

plt.title("Memory Usage During Allocation and Garbage Collection", fontsize=14, fontweight='bold')
plt.xlabel("Iteration", fontsize=12)
plt.ylabel("Memory Usage (MB)", fontsize=12)
plt.legend(loc="upper left", fontsize=10)
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()
