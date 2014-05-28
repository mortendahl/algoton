




#####################
#
#  Heap structure, for min-heaps and max-heaps
#
#
#  - Cormen et al., section 6.1-6.3
#
#  - example:
#     - max-heap [16,14,10,8,7,9,3,2,4,1] has tree structure:
#
#                               16 [0]
#                   14 [1]                  10 [2]
#           8 [3]           7 [4]       9 [5]       3 [6]
#       2 [7]    4 [8]  1 [9]   
#
#      - i.e. each node is bigger than all of its children
#      - note that this does NOT imply that then array is sorted
#      - ... nor that it is a binary search tree
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
    #  - worst-case running time is O(h_i) where h_i = ln n is height of tree rooted at i
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
    #  - worst-case running time is O(n), see Cormen et al. p133-135
    def build_max_heap(self):
        arraysize = len(self._heap)
        self._heapsize = arraysize
        # the last parent must be at index 'lastparent' mid-way in the array 
        #  - since 'left(lastparent)' and 'right(lastparent)' would overflow
        lastparent = (arraysize // 2) - 1
        # loop from 'lastparent' down to 0 (root)
        # loop-invariant: 'i' is the root of a max-heap
        for i in xrange(lastparent, -1, -1):
            self.max_heapify(i)

    # sorts the underlying list in increasing order
    #  - worst-case running time is O(n * lg n)
    def sort_increasing(self):
        self.build_max_heap()
        # loop-invariant: heap[i..] contains the (n-i)th largest numbers in sorted order
        for i in xrange(len(self._heap)-1, 0, -1):
            # swap trick from stack overflow
            #  - supposedly works because Python first evaluates all of the right side
            #  - uses two temp variables instead of one, but easier to read
            self._heap[0], self._heap[i] = self._heap[i], self._heap[0]
            self._heapsize -= 1
            self.max_heapify(0)
        # at this point there's only one item left in the heap, at the root, which must 
        # be the smallest element and located at heap[0] -- hence heap[0..] is sorted









class MinHeap(Heap):
    
    def __init__(self, heap=[]):
        Heap.__init__(self, heap)
    
    # turns heap at i into min-heap
    #  - assuming heaps at left(i) and right(i) are min-heaps
    #  - worst-case running time is O(h_i) where h_i = ln n is height of tree rooted at i
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
    #  - worst-case running time is O(n), see Cormen et al. p133-135
    def build_min_heap(self):
        arraysize = len(self._heap)
        self._heapsize = arraysize
        # the last parent must be at index 'lastparent' mid-way in the array 
        #  - since 'left(lastparent)' and 'right(lastparent)' would overflow
        lastparent = (arraysize // 2) - 1
        # loop from 'lastparent' down to 0 (root)
        # loop-invariant: 'i' is the root of a min-heap
        for i in xrange(lastparent, -1, -1):
            self.min_heapify(i)
            
    # sorts the underlying list in decreasing order
    #  - worst-case running time is O(n * lg n)
    def sort_decreasing(self):
        self.build_min_heap()
        # loop-invariant: heap[i..] contains the (n-i)th smallest numbers in sorted order
        for i in xrange(len(self._heap)-1, 0, -1):
            # swap trick from stack overflow
            #  - supposedly works because Python first evaluates all of the right side
            #  - uses two temp variables instead of one, but easier to read
            self._heap[0], self._heap[i] = self._heap[i], self._heap[0]
            self._heapsize -= 1
            self.min_heapify(0)
        # at this point there's only one item left in the heap, at the root, which must 
        # be the largest element and located at heap[0] -- hence heap[0..] is sorted











# all methods assume we have a max-heap
#  - see http://docs.python.org/2/library/exceptions.html for reason behind choice of exception

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
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        

######################
#
#  Dijkstra (Cormen et al. section ...)
#
#















