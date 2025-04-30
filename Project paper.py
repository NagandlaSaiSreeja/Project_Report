
import time
import matplotlib.pyplot as plt
import pandas as pd

class Element:
    def __init__(self, value):
        self.value = value
        self.next = None
        self.set_ref = None

class LinkedListSet:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def append(self, element):
        if self.head is None:
            self.head = self.tail = element
        else:
            self.tail.next = element
            self.tail = element
        element.set_ref = self
        self.size += 1

class DisjointSet:
    def __init__(self):
        self.elements = {}

    def make_set(self, value):
        element = Element(value)
        set_instance = LinkedListSet()
        set_instance.append(element)
        self.elements[value] = element

    def find_set(self, value):
        return self.elements[value].set_ref.head.value

    def union(self, val1, val2):
        elem1 = self.elements[val1]
        elem2 = self.elements[val2]
        set1 = elem1.set_ref
        set2 = elem2.set_ref

        if set1 == set2:
            return

        if set1.size < set2.size:
            set1, set2 = set2, set1

        current = set2.head
        while current:
            next_node = current.next
            set1.append(current)
            current = next_node

        set2.head = set2.tail = None
        set2.size = 0

def benchmark(n):
    ds = DisjointSet()
    for i in range(n):
        ds.make_set(i)

    start_union = time.time()
    for i in range(n - 1):
        ds.union(i, i + 1)
    end_union = time.time()

    start_find = time.time()
    for i in range(n):
        ds.find_set(i)
    end_find = time.time()

    return end_union - start_union, end_find - start_find

def plot_performance():
    sizes = [100, 500, 1000, 2000, 4000, 8000]
    union_times = []
    find_times = []

    for size in sizes:
        u_time, f_time = benchmark(size)
        union_times.append(u_time)
        find_times.append(f_time)

    data = pd.DataFrame({
        'Elements': sizes,
        'Union Time (s)': union_times,
        'Find Time (s)': find_times
    })

    print("\nPerformance Table:")
    print(data.to_string(index=False))

    plt.figure()
    plt.plot(sizes, union_times, label='Union Time', marker='o')
    plt.plot(sizes, find_times, label='Find Time', marker='s')
    plt.xlabel('Number of Elements')
    plt.ylabel('Time (seconds)')
    plt.title('Performance of Linked-List Disjoint Set Operations')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

plot_performance()