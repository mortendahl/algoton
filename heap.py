






#
# heap structure, for min-heaps and max-heaps
#
class Heap:
    
    def __init__(self, heap=[]):
        self._heap = heap
        self._heapsize = len(heap)
        
    def value(self, i):
        return _heap[i]
        
    def parent(self, i):
        return (i-1) // 2

    def left(self, i):
        return 2*i + 1

    def right(self, i):
        return 2*i + 2

    def print_list(self):
        print self._heap[:self._heapsize]

    def print_full_list(self):
        print self._heap

    def print_tree(self, i=0, indent="", step="  "):
        if not i < self._heapsize: return
        print "{0}{1} [{2}]".format(indent, self._heap[i], i)
        self.print_tree(self.left(i), indent+step)
        self.print_tree(self.right(i), indent+step)














class MaxHeap(Heap):
    
    def __init__(self, heap=[]):
        Heap.__init__(self, heap)
        
    # turns heap at i into max-heap
    #  - assuming heaps at left(i) and right(i) are max-heaps
    #  - worst-case running time is O(h) where h = ln n is height of tree rooted at i
    def max_heapify(self, i):
        largest = i
        l = self.left(i)
        if l < self._heapsize and self._heap[l] > self._heap[i]: largest = l
        r = self.right(i)
        if r < self._heapsize and self._heap[r] > self._heap[largest]: largest = r
        if largest != i:
            # swap trick from stack overflow
            #  - supposedly works because Python first evaluates all of the right side
            #  - uses two temp variables instead of one, but easier to read
            self._heap[i], self._heap[largest] = self._heap[largest], self._heap[i]
            self.max_heapify(largest)
    
    # transforms array into max-heap
    #  - worst-case running time is O(n)
    def build_max_heap(self):
        arraysize = len(self._heap)
        self._heapsize = arraysize
        # the last parent must be at index i mid-way in the array since left(i)/right(i) would overflow
        lastparent = (arraysize // 2) - 1
        # loop from 'lastparent' down to 0
        for i in xrange(lastparent, -1, -1):
            self.max_heapify(i)

    # sorts the underlying list in increasing order
    #  - worst-case running time is O(n * lg n)
    def sort_increasing(self):
        self.build_max_heap()
        for i in xrange(len(self._heap)-1, 0, -1):
            # swap trick from stack overflow
            #  - supposedly works because Python first evaluates all of the right side
            #  - uses two temp variables instead of one, but easier to read
            self._heap[0], self._heap[i] = self._heap[i], self._heap[0]
            self._heapsize -= 1
            self.max_heapify(0)














class MinHeap(Heap):
    
    def __init__(self, heap=[]):
        Heap.__init__(self, heap)
    
    # turns heap at i into min-heap
    #  - assuming heaps at left(i) and right(i) are min-heaps
    #  - worst-case running time is O(h) where h = ln n is height of tree rooted at i
    def min_heapify(self, i):
        smallest = i
        l = self.left(i)
        if l < self._heapsize and self._heap[l] < self._heap[i]: smallest = l
        r = self.right(i)
        if r < self._heapsize and self._heap[r] < self._heap[smallest]: smallest = r
        if smallest != i:
            # swap trick from stack overflow
            #  - supposedly works because Python first evaluates all of the right side
            #  - uses two temp variables instead of one, but easier to read
            self._heap[i], self._heap[smallest] = self._heap[smallest], self._heap[i]
            self.min_heapify(smallest)

    # transforms array into min-heap
    #  - worst-case running time is O(n)
    def build_min_heap(self):
        arraysize = len(self._heap)
        self._heapsize = arraysize
        # the last parent must be at index i mid-way in the array since left(i)/right(i) would overflow
        lastparent = (arraysize // 2) - 1
        # loop from 'lastparent' down to 0
        for i in xrange(lastparent, -1, -1):
            self.min_heapify(i)
            
    # sorts the underlying list in decreasing order
    #  - worst-case running time is O(n * lg n)
    def sort_decreasing(self):
        self.build_min_heap()
        # smallest element at root, so 
        for i in xrange(len(self._heap)-1, 0, -1):
            # swap trick from stack overflow
            #  - supposedly works because Python first evaluates all of the right side
            #  - uses two temp variables instead of one, but easier to read
            self._heap[0], self._heap[i] = self._heap[i], self._heap[0]
            self._heapsize -= 1
            self.min_heapify(0)
