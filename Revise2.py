import gc
import random
import psutil
import time
import matplotlib.pyplot as plt
import seaborn as sns
from collections import deque

# Configure Seaborn for aesthetics
sns.set(style="whitegrid", palette="coolwarm")

# Deque to hold memory usage snapshots
memory_log = deque(maxlen=5)

def allocate_memory(num_objects=10000, list_size=100):
    """
    Allocate memory by creating a list of lists filled with random floats.
    """
    return [[random.random() for _ in range(list_size)] for _ in range(num_objects)]

def get_memory_usage_mb():
    """
    Get current process memory usage in MB.
    """
    return psutil.Process().memory_info().rss / (1024 * 1024)

def monitor_memory():
    """
    Monitor memory usage before allocation, after allocation, and after GC.
    Logs the result in memory_log.
    """
    mem_before = get_memory_usage_mb()
    temp_data = allocate_memory()
    mem_after_alloc = get_memory_usage_mb()
    
    del temp_data  # Remove references
    gc.collect()   # Force garbage collection
    
    mem_after_gc = get_memory_usage_mb()
    memory_log.append((mem_before, mem_after_alloc, mem_after_gc))

# Run memory monitoring for 5 cycles
for _ in range(5):
    monitor_memory()
    time.sleep(1)

# Prepare data for plotting
iterations = list(range(1, len(memory_log) + 1))
mem_before_list = [entry[0] for entry in memory_log]
mem_after_alloc_list = [entry[1] for entry in memory_log]
mem_after_gc_list = [entry[2] for entry in memory_log]

# Plot the memory usage across iterations
plt.figure(figsize=(10, 6))
plt.plot(iterations, mem_before_list, marker='o', linestyle='--', linewidth=2, label='Before Allocation')
plt.plot(iterations, mem_after_alloc_list, marker='s', linestyle=':', linewidth=2, label='After Allocation')
plt.plot(iterations, mem_after_gc_list, marker='^', linestyle='-', linewidth=2, label='After GC')

# Labels and title
plt.xlabel("Iteration", fontsize=12, fontweight='bold')
plt.ylabel("Memory Usage (MB)", fontsize=12, fontweight='bold')
plt.title("Garbage Collection Impact on Memory Usage", fontsize=14, fontweight='bold')
plt.legend(loc='upper left', fontsize=10, fancybox=True, shadow=True)
plt.grid(True, linestyle='--', alpha=0.6)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
plt.tight_layout()
plt.show()
