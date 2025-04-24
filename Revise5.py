import gc
import random
import psutil
import time
import matplotlib.pyplot as plt
import seaborn as sns
from collections import deque

# ------------------------------
# Configuration
# ------------------------------

NUM_ITERATIONS = 5
OBJECT_COUNT = 10_000
LIST_SIZE = 100

# Memory tracking buffer (FIFO)
memory_log = deque(maxlen=NUM_ITERATIONS)

# Set seaborn style
sns.set(style="whitegrid", palette="coolwarm")

# ------------------------------
# Memory Functions
# ------------------------------

def get_memory_mb():
    """Return current process memory usage in MB."""
    process = psutil.Process()
    return process.memory_info().rss / (1024 * 1024)

def allocate_temp_memory(count=OBJECT_COUNT, size=LIST_SIZE):
    """Allocate temporary memory by generating nested lists."""
    return [[random.random() for _ in range(size)] for _ in range(count)]

def record_memory_cycle():
    """Track memory usage before allocation, after allocation, and after GC."""
    mem_before = get_memory_mb()

    temp = allocate_temp_memory()
    mem_after_alloc = get_memory_mb()

    del temp
    gc.collect()

    mem_after_gc = get_memory_mb()
    memory_log.append((mem_before, mem_after_alloc, mem_after_gc))

# ------------------------------
# Execution Loop
# ------------------------------

for _ in range(NUM_ITERATIONS):
    record_memory_cycle()
    time.sleep(1)

# ------------------------------
# Data Extraction
# ------------------------------

iterations = list(range(1, len(memory_log) + 1))
mem_before = [entry[0] for entry in memory_log]
mem_after_alloc = [entry[1] for entry in memory_log]
mem_after_gc = [entry[2] for entry in memory_log]

# ------------------------------
# Plotting
# ------------------------------

plt.figure(figsize=(10, 6))

plt.plot(iterations, mem_before, label="Before Allocation", marker='o', linestyle='--', linewidth=2)
plt.plot(iterations, mem_after_alloc, label="After Allocation", marker='s', linestyle=':', linewidth=2)
plt.plot(iterations, mem_after_gc, label="After Garbage Collection", marker='^', linestyle='-', linewidth=2)

plt.title("Memory Usage During Allocation and Garbage Collection", fontsize=14, fontweight='bold')
plt.xlabel("Iteration", fontsize=12)
plt.ylabel("Memory (MB)", fontsize=12)
plt.legend(loc="upper left", fontsize=10)
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()
