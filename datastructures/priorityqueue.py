


# all methods assume we have a max-heap
#  - see http://docs.python.org/2/library/exceptions.html for reason behind choice of exception

from heap import MaxHeap

class MaxPriorityQueue(MaxHeap):
    
    def __init__(self, heap=[]):
        MaxHeap.__init__(self, heap)

    def maximum(self):
        return self._heap[0]
        
    def extract_max(self):
        if self._heapsize < 1: return None
        max = self._heap[0]
        # remove current max and replace with one of the smallest numbers
        self._heap[0] = self._heap[self._heapsize - 1]
        self._heapsize -= 1
        # find next maximum element
        self.max_heapify(0)
        return max
        
    def increase_key(self, i, key):
        if key < self._heap[i]: raise ValueError("New key is smaller than current key")
        # traverse towards the top for the right location, swapping elements on the way
        while i > 0 and self._heap[self.parent(i)] < key:
            self._heap[i] = self._heap[self.parent(i)]
            i = self.parent(i)
        # update value at the index we found
        self._heap[i] = key
        
    def decrease_key(self, i, key):
        if key > self._heap[i]: raise ValueError("New key is larger than current key")
        # update current index
        self._heap[i] = key
        self.max_heapify(i)

    def insert(self, key):
        if not self._heapsize < len(self._heap): raise ValueError("Not enough room in array")
        self._heapsize += 1
        # traverse towards the top for the right location, swapping elements on the way
        i = self._heapsize - 1
        while i > 0 and self._heap[self.parent(i)] < key:
            self._heap[i] = self._heap[self.parent(i)]
            i = self.parent(i)
        # update value at the index we found
        self._heap[i] = key
        














# all methods assume we have a min-heap
#  - see http://docs.python.org/2/library/exceptions.html for reason behind choice of exception

from heap import MinHeap

class MinPriorityQueue(MinHeap):
    
    def __init__(self, heap=[]):
        MinHeap.__init__(self, heap)
        
    def minimum(self):
        return self._heap[0]
        
    def extract_min(self):
        if self._heapsize < 1: return None
        min = self._heap[0]
        # remove current min and replace with one of the largest numbers
        self._heap[0] = self._heap[self._heapsize - 1]
        self._heapsize -= 1
        # find next minimum element
        self.min_heapify(0)
        return min
        
    def decrease_key(self, i, key):
        if key > self._heap[i]: raise ValueError("New key is larger than current key")
        # traverse towards the top for the right location, swapping elements on the way
        while i > 0 and self._heap[self.parent(i)] > key:
            self._heap[i] = self._heap[self.parent(i)]
            i = self.parent(i)
        # update value at the index we found
        self._heap[i] = key
    
    def increase_key(self, i, key):
        if key < self._heap[i]: raise ValueError("New key is smaller than current key")
        # update current index
        self._heap[i] = key
        self.min_heapify(i)
        
    def insert(self, key):
        if not self._heapsize < len(self._heap): raise ValueError("Not enough room in array")
        self._heapsize += 1
        # traverse towards the top for the right location, swapping elements on the way
        i = self._heapsize - 1
        while i > 0 and self._heap[self.parent(i)] > key:
            self._heap[i] = self._heap[self.parent(i)]
            i = self.parent(i)
        # update value at the index we found
        self._heap[i] = key
        
        