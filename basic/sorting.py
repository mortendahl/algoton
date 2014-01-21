

#####################
#
#  Insertion sort 
#
#
#  - Cormen et al. p15-27
#
#  - example:
#     - j=1, i=0: [2,4,1,3], [2,4,1,3]
#     - j=2, i=1: [2,4,1,3], i=0: [2,4,4,3], i=-1: [2,2,4,3], [1,2,4,3]
#     - j=3, i=2: [1,2,4,3], i=1: [1,2,4,4], [1,2,3,4]
#
#  - worst case: O(n**2), when already sorted in decreasing order all elements willl be shifted
#  - best case: O(n), when already sorted so no shifting
#  - average case: half of worst case, since for each element, half will be higher so half will be shifted
#  - space: in-place
#

def insertion_sort(numbers):
	# from head to tail
	# loop-invariant: sub-array numbers[0..j-1] sorted
	for j in xrange(1, len(numbers)):
		key = numbers[j]
		i = j - 1
		# from current index to head, find index for 'key' and shift larger elements
		while i >= 0 and numbers[i] > key:
			numbers[i+1] = numbers[i]
			i = i - 1
		numbers[i+1] = key











#####################
#
#  Merge sort
#
#
#  - Cormen et al. p28-36
#
#  - example:
#    merge_sort([4,2,3,1], p=0, r=3): q = 1
#                *******
#      merge_sort([4,2,3,1], p=0, r=1): q = 0
#                  ***
#        merge_sort([4,2,3,1], p=0, r=0)
#                    *
#        merge_sort([4,2,3,1], p=1, r=1)
#                      *
#        _merge_sort_merge([4,2,3,1], p=0, q=1, r=1): k=0: [2,2,3,1], k=1: [2,4,3,1]
#                           ***
#      merge_sort([2,4,3,1], p=2, r=3): q = 2:
#                      ***
#        merge_sort([2,4,3,1], p=2, r=2)
#                        *
#        merge_sort([2,4,3,1], p=3, r=3)
#                          *
#        _merge_sort_merge([2,4,3,1], p=2, q=3, r=3): k=2: [2,4,1,1], k=3: [2,4,1,3]
#                               ***
#      _merge_sort_merge([2,4,1,3], p=0, q=2, r=3): k=0: [1,4,1,3], k=1: [1,2,1,3], k=2: [1,2,3,3], k=3: [1,2,3,4]
#                         *******
#
#  - worst case: O(n * lg n)
#  - best case: O(n * lg n), since nothing makes it stop prematurely
#  - average case: O(n * lg n), since nothing makes it strop prematurely
#  - space: O(n), since in top step the entire list is copied in _merge_sort_merge
#
#  - notes: 
#     - because of the use of recursion, we might exhaust the stack; however, this seems to happen only 
#       around depth 1000, which means the list must have length around 2**1000, i.e. astronomical
#

# assumes that 'numbers[p:q]' and 'numbers[q:r+1]' are both already sorted increasingly
# afterwards 'numbers[p:r+1]' are sorted increasingly
def _merge_sort_merge(numbers, p, q, r):
	# important that both sub-arrays are copied here since 'numbers[p:r+1]' will be overridden below
	left = numbers[p:q]
	right = numbers[q:r+1]
	# start at head of each sub-array
	i = 0
	j = 0
	# repeated pick the smallest element from the two sub-arrays
	# loop-invariant: sub-array 'numbers[p..k-1]' contains 'k-p' smallest elements of 'left' and 'right', sorted
	for k in xrange(p, r+1):
		if not i < len(left):
			# we have exhausted 'left' so the rest must be in 'right'
			numbers[k] = right[j]
			j += 1
		elif not j < len(right):
			# we have exhausted 'right' so the rest must be in 'left'
			numbers[k] = left[i]
			i += 1
		elif left[i] <= right[j]:
			# pick the next element in 'left', as it is at least as small as the next in 'right'
			numbers[k] = left[i]
			i += 1
		else:
			# pick the next element in 'right', as it is smaller than the next in 'left'
			numbers[k] = right[j]
			j += 1

def merge_sort(numbers, p=0, r=None):
	if r == None: r = len(numbers) - 1
	if p < r:
		q = (p + r) // 2
		# sort left branch
		merge_sort(numbers, p, q)
		# sort right branch
		merge_sort(numbers, q+1, r)
		# merge the two sorted branches
		_merge_sort_merge(numbers, p, q+1, r)











#####################
#
#  Bubble sort
#
#
#  - Cormen et al. p38
#
#  - example:
#     - i=0, j=3: [2,4,1,3] -> [2,4,1,3]
#            j=2: -> [2,1,4,3]
#            j=1: -> [1,2,4,3]
#     - i=1, j=3: -> [1,2,3,4]
#            j=2: -> [1,2,3,4]
#     - i=2, j=3: -> [1,2,3,4]
#
#  - worst case: O(n**2)
#  - best case: O(n**2), since nothing makes it stop prematurely
#  - average case: O(n**2), since nothing makes it strop prematurely
#  - space: in-place
#

def bubble_sort(numbers):
	# loop-invariant: sub-array numbers[0..i] contains the i+1 smallest numbers, sorted increasingly
	for i in xrange(len(numbers)-1):
		# loop-invariant: numbers[j-1] smaller than all numbers in sub-array numbers[j..]
		for j in xrange(len(numbers)-1, i, -1):
			if numbers[j] < numbers[j - 1]:
				temp = numbers[j]
				numbers[j] = numbers[j - 1]
				numbers[j - 1] = temp


# we can optimise slightly, breaking if nothing was swapped in the inner for-loop:
#  - numbers[0..i-1] already sorted and smaller than any in numbers[i..] by previous iteration
#  - this implies numbers[0] < .. < numbers[i]
#  - since nothing was swapped we also have numbers[j-1] < numbers[j] for j in i+1,...,len(numbers)-1
#  - this implies numbers[i] < .. < numbers[len(..)-1]
# 
# best case: O(n), when already sorted
#
def bubble_sort_optimised(numbers):
	for i in xrange(len(numbers)-1):
		swapped = False
		for j in xrange(len(numbers)-1, i, -1):
			if numbers[j] < numbers[j - 1]:
				temp = numbers[j]
				numbers[j] = numbers[j - 1]
				numbers[j - 1] = temp
				swapped = True
		if not swapped: return









#
# best case: O(n * lg n)
#
# worst case: O(n * lg n)
#
# average case: O(n * lg n)
#
def subset2_sum(list_of_numbers, target):
	merge_sort(list_of_numbers)   # sorted in-place
	lower = 0
	upper = len(list_of_numbers) - 1
	while lower < upper:
		current = list_of_numbers[lower] + list_of_numbers[upper]
		if target == current:
			# found solution
			return list_of_numbers[lower], list_of_numbers[upper]
		elif target > current:
			# move 'lower' up
			lower += 1
		elif target < current:
			# move 'upper' down
			upper -= 1
	return None












#
# best case: O(lg n)
#
# worst case: O(lg n)
#
# average case: O(lg n)
#
# notes:
#  - assumes 'numbers' to be sorted in increasing order
#
def binary_search_mustbe_recursive(numbers, target, lower=0, upper=None):
	if upper == None: upper = len(numbers) - 1
	# check if we're at the bottom
	if lower == upper:
		if target == numbers[lower]: return lower
		else: return None
	# not at bottom yet, jump mid-way
	middle = (lower + upper) // 2
	if target == numbers[middle]:
		# found 'target'
		return middle
	elif target < numbers[middle]:
		# look in left half
		return binary_search_mustbe_recursive(numbers, target, lower, middle)
	else:
		# look in right half
		return binary_search_mustbe_recursive(numbers, target, middle + 1, upper)
		

def binary_search_mustbe_iterative(numbers, target, lower=0, upper=None):
	if upper == None: upper = len(numbers) - 1
	while lower < upper:
		middle = (lower + upper) // 2
		if target == numbers[middle]:
			return middle
		elif target < numbers[middle]:
			#lower = lower
			upper = middle
		else:
			lower = middle + 1
			#upper = upper
	# here, lower == upper (or lower > upper, in which case you're just stupid)
	if target == numbers[lower]: return lower
	else: return None
	
	
def binary_search_shouldbe_recursive(numbers, target, lower=0, upper=None):
	if upper == None: upper = len(numbers) - 1
	# check if we're at the bottom
	if lower == upper:
		return lower
	# not at bottom yet, jump mid-way
	middle = (lower + upper) // 2
	if target == numbers[middle]:
		# found 'target'
		return middle
	elif target < numbers[middle]:
		# look in left half
		return binary_search_shouldbe_recursive(numbers, target, lower, middle)
	else:
		# look in right half
		return binary_search_shouldbe_recursive(numbers, target, middle + 1, upper)


def binary_search_shouldbe_iterative(numbers, target, lower=0, upper=None):
	if upper == None: upper = len(numbers) - 1
	while lower < upper:
		middle = (lower + upper) // 2
		if target == numbers[middle]:
			return middle
		elif target < numbers[middle]:
			upper = middle
		else:
			lower = middle + 1
	# here, lower == upper (or lower > upper, in which case you're just stupid)
	return lower











#
# best case: O(lg n)
#
# worst case: O(lg n)
#
# average case: O(lg n)
#
# notes:
#  - assumes 'numbers' to be sorted in increasing order
#
def closest_match(numbers, target):
	index = binary_search_shouldbe_iterative(numbers, target)
	if target == numbers[index]: return index
	elif target < numbers[index]:
		# look here, or next different numbers on the left
		neighbourIndex = index
		while numbers[index] == numbers[neighbourIndex] and neighbourIndex > 0:
			neighbourIndex -= 1
		if abs(target - numbers[neighbourIndex]) < abs(target - numbers[index]):
			return neighbourIndex
		else:
			return index
	else:
		# look here, or next different numbers on the right
		neighbourIndex = index
		while numbers[index] == numbers[neighbourIndex] and neighbourIndex < len(numbers) - 1:
			neighbourIndex += 1
		if abs(target - numbers[neighbourIndex]) < abs(target - numbers[index]):
			return neighbourIndex
		else:
			return index







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
	
	
	###################
	#  for heap_sort  #
	###################
	
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
		
	
	############################
	#  for max-priority queue  #
	############################
		
	# assumes we have a max-heap
	def max_maximum(self):
		return self._heap[0]
		
	# assumes we have a max-heap
	def max_extract(self):
		if self._heapsize < 1: return None
		max = self._heap[0]
		# remove current max and replace with one of the smallest numbers
		self._heap[0] = self._heap[self._heapsize - 1]
		self._heapsize -= 1
		# find next maximum element
		self.max_heapify(0)
		return max
		
	# assumes we have a max-heap
	#  - see http://docs.python.org/2/library/exceptions.html for reason behind choice of exception
	def max_increase_key(self, i, key):
		if key < self._heap[i]: raise ValueError("New key is smaller than current key")
		# traverse towards the top for the right location, swapping elements on the way
		while i > 0 and self._heap[self.parent(i)] < key:
			self._heap[i] = self._heap[self.parent(i)]
			i = self.parent(i)
		# update value at the index we found
		self._heap[i] = key
		
	# assumes we have a max-heap
	def max_decrease_key(self, i, key):
		if key > self._heap[i]: raise ValueError("New key is larger than current key")
		# update current index
		self._heap[i] = key
		self.max_heapify(i)
		
	# assumes we have a max-heap
	#  - see http://docs.python.org/2/library/exceptions.html for reason behind choice of exception
	def max_insert(self, key):
		if not self._heapsize < len(self._heap): raise ValueError("Not enough room in array")
		self._heapsize += 1
		# traverse towards the top for the right location, swapping elements on the way
		i = self._heapsize - 1
		while i > 0 and self._heap[self.parent(i)] < key:
			self._heap[i] = self._heap[self.parent(i)]
			i = self.parent(i)
		# update value at the index we found
		self._heap[i] = key
		
		
	############################
	#  for min-priority queue  #
	############################
		
	# assumes we have a min-heap	
	def min_minimum(self):
		return self._heap[0]
		
	# assumes we have a min-heap
	def min_extract(self):
		if self._heapsize < 1: return None
		min = self._heap[0]
		# remove current min and replace with one of the largest numbers
		self._heap[0] = self._heap[self._heapsize - 1]
		self._heapsize -= 1
		# find next minimum element
		self.min_heapify(0)
		return min
		
	# assumes we have a min-heap
	#  - see http://docs.python.org/2/library/exceptions.html for reason behind choice of exception
	def min_decrease_key(self, i, key):
		if key > self._heap[i]: raise ValueError("New key is larger than current key")
		# traverse towards the top for the right location, swapping elements on the way
		while i > 0 and self._heap[self.parent(i)] > key:
			self._heap[i] = self._heap[self.parent(i)]
			i = self.parent(i)
		# update value at the index we found
		self._heap[i] = key
	
	# assumes we have a min-heap
	def min_increase_key(self, i, key):
		if key < self._heap[i]: raise ValueError("New key is smaller than current key")
		# update current index
		self._heap[i] = key
		self.min_heapify(i)
		
	# assumes we have a min-heap
	#  - see http://docs.python.org/2/library/exceptions.html for reason behind choice of exception
	def min_insert(self, key):
		if not self._heapsize < len(self._heap): raise ValueError("Not enough room in array")
		self._heapsize += 1
		# traverse towards the top for the right location, swapping elements on the way
		i = self._heapsize - 1
		while i > 0 and self._heap[self.parent(i)] > key:
			self._heap[i] = self._heap[self.parent(i)]
			i = self.parent(i)
		# update value at the index we found
		self._heap[i] = key
		
		

#
# best case: O(n * lg n)
#
# worst case: O(n * lg n)
#
# average case: O(n * lg n)
#
# amortised: only invoked once
#
def heap_sort(list_to_sort):
	heap = Heap(list_to_sort)
	heap.sort_max()
