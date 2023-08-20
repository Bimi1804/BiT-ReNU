import time
from memory_profiler import memory_usage

def test_function():
    # Just an example function that creates a list of squares
    return [i * i for i in range(100000)]

def measure_function(func):
    start_time = time.time()
    # Measure memory usage. The returned result is a list of memory consumption 
    # values in MiB every 'interval' seconds (here 0.1 seconds)
    mem_usage = memory_usage((func, ), interval=0.1)
    end_time = time.time()
    exec_time = end_time - start_time
    # We'll return the maximum memory usage during the function execution and 
    # the total execution time. 
    # Note: mem_usage might contain only a single value if your function is very fast.
    return max(mem_usage), exec_time

if __name__ == '__main__':
    # Assuming that the existing script's main code starts from this point
    memory, duration = measure_function(test_function)
    print(f"Memory used: {memory:.2f} MiB")
    print(f"Execution time: {duration:.2f} seconds")
