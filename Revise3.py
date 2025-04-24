import gc
import random
import psutil
import time
import matplotlib.pyplot as plt
import seaborn as sns
from collections import deque

# Set up for visualization
sns.set(style="whitegrid", palette="coolwarm")

# Initialize a fixed-size memory usage log
memory_records = deque(maxlen=5)

def allocate_objects(count=10000, size=100):
    """Allocate memory-heavy objects (list of random floats)."""
    return [[random.random() for _ in range(size)] for _ in range(count)]

def current_memory_mb():
    """Get current memory usage of the process in MB."""
    process = psutil.Process()
    return process.memory_info().rss / (1024 * 1024)

def track_memory():
    """Record memory usage before, during, and after allocation + GC."""
    before = current_memory_mb()
    data = allocate_objects()
    after_alloc = current_memory_mb()

    del data
    gc.collect()
    after_gc = current_memory_mb()

    memory_records.append((before, after_alloc, after_gc))

# Run the tracker multiple times
for _ in range(5):
    track_memory()
    time.sleep(1)

# Prepare data for plotting
iterations = list(range(1, len(memory_records) + 1))
before_list = [m[0] for m in memory_records]
allocated_list = [m[1] for m in memory_records]
after_gc_list = [m[2] for m in memory_records]

# Plot the results
plt.figure(figsize=(10, 6))
plt.plot(iterations, before_list, label="Before Allocation", marker='o', linestyle='--', linewidth=2)
plt.plot(iterations, allocated_list, label="After Allocation", marker='s', linestyle=':', linewidth=2)
plt.plot(iterations, after_gc_list, label="After GC", marker='^', linestyle='-', linewidth=2)

plt.title("Memory Usage Before and After Garbage Collection", fontsize=14, fontweight='bold')
plt.xlabel("Iteration", fontsize=12)
plt.ylabel("Memory (MB)", fontsize=12)
plt.legend(loc="upper left", fontsize=10)
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()
