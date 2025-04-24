import gc
import random
import psutil
import time
import matplotlib.pyplot as plt
import seaborn as sns
from collections import deque

# Queue to store memory usage over multiple iterations
memory_queue = deque(maxlen=5)

def allocate_memory(num_objects=10000):
    """Simulates memory allocation by creating a list of random lists."""
    return [[random.random() for _ in range(100)] for _ in range(num_objects)]

def get_memory_usage():
    """Returns the current memory usage of the process in MB."""
    return psutil.Process().memory_info().rss / (1024 * 1024)

def monitor_gc():
    """Monitors memory usage before allocation, after allocation, and after garbage collection."""
    memory_before = get_memory_usage()
    objects = allocate_memory()
    memory_allocated = get_memory_usage()
    del objects  # Remove references to allocated memory
    gc.collect()  # Force garbage collection
    memory_after_gc = get_memory_usage()
    memory_queue.append((memory_before, memory_allocated, memory_after_gc))

# Run monitoring for 5 iterations
for _ in range(5):
    monitor_gc()
    time.sleep(1)

# Extract memory data for plotting
memory_before = [entry[0] for entry in memory_queue]
memory_allocated = [entry[1] for entry in memory_queue]
memory_after_gc = [entry[2] for entry in memory_queue]
iterations = list(range(1, len(memory_queue) + 1))

# Set plot style and configuration
sns.set_style("whitegrid")
sns.set_palette("coolwarm")

plt.figure(figsize=(10, 6))
sns.lineplot(x=iterations, y=memory_before, label="Before Allocation", marker='o', linestyle='dashed', linewidth=2)
sns.lineplot(x=iterations, y=memory_allocated, label="After Allocation", marker='s', linestyle='dotted', linewidth=2)
sns.lineplot(x=iterations, y=memory_after_gc, label="After GC", marker='^', linestyle='solid', linewidth=2)

# Labeling the plot
plt.xlabel("Iteration", fontsize=12, fontweight='bold')
plt.ylabel("Memory Usage (MB)", fontsize=12, fontweight='bold')
plt.title("Efficient Garbage Collection in OS (FIFO-based Tracking)", fontsize=14, fontweight='bold')
plt.legend(fontsize=10, fancybox=True, shadow=True, loc="upper left")
plt.grid(True, linestyle='--', alpha=0.6)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
plt.tight_layout()
plt.show()
