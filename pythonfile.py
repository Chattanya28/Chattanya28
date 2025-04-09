import gc
import random
import psutil
import time
import matplotlib.pyplot as plt
import seaborn as sns
from collections import deque
memory_queue = deque(maxlen=5)
def allocate_memory(num_objects=10000):
    objects = []
    for _ in range(num_objects):
        objects.append([random.random() for _ in range(100)])  # Creating random lists
    return objects
def get_memory_usage():
    return psutil.Process().memory_info().rss / (1024 * 1024)  # Convert bytes to MB
def monitor_gc():
    memory_before = get_memory_usage()
    objects = allocate_memory()
    memory_allocated = get_memory_usage()
    del objects  # Remove references
    gc.collect()  # Force garbage collection
    memory_after_gc = get_memory_usage()
     memory_queue.append((memory_before, memory_allocated, memory_after_gc))
for _ in range(5):
    monitor_gc()
    time.sleep(1)
memory_before = [entry[0] for entry in memory_queue]
memory_allocated = [entry[1] for entry in memory_queue]
memory_after_gc = [entry[2] for entry in memory_queue]
iterations = list(range(1, len(memory_queue) + 1))
sns.set_style("whitegrid")
sns.set_palette("coolwarm")
plt.figure(figsize=(10, 6))
sns.lineplot(x=iterations, y=memory_before, label="Before Allocation", marker='o', linestyle='dashed', linewidth=2)
sns.lineplot(x=iterations, y=memory_allocated, label="After Allocation", marker='s', linestyle='dotted', linewidth=2)
sns.lineplot(x=iterations, y=memory_after_gc, label="After GC", marker='^', linestyle='solid', linewidth=2)
plt.xlabel("Iteration", fontsize=12, fontweight='bold')
plt.ylabel("Memory Usage (MB)", fontsize=12, fontweight='bold')
plt.title("Efficient Garbage Collection in OS (FIFO-based Tracking)", fontsize=14, fontweight='bold')
plt.legend(fontsize=10, fancybox=True, shadow=True, loc="upper left")
plt.grid(True, linestyle='--', alpha=0.6)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
plt.show()

//2nd revise
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

//3rd revise

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


//4th revise
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


//5th revise
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


//6th revise
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
