

#
# best case: O(n), when already sorted so no shifting
#
# worst case: O(n**2), when already sorted in decreasing order all elements willl be shifted
#
# average case: half of worst case, since for each element, half will be higher so half will be shifted
#
# amortised: only invoked once
#
# space: in-place
#
def insertion_sort(list_to_sort):
	# from head to tail
	for j in xrange(1, len(list_to_sort)):
		key = list_to_sort[j]
		i = j - 1
		# from current index to head, find index for 'key' and shift larger elements
		while i >= 0 and list_to_sort[i] > key:
			list_to_sort[i+1] = list_to_sort[i]
			i = i - 1
		list_to_sort[i+1] = key











#
# best case: O(n * lg n)
#
# worst case: O(n * lg n)
#
# average case: O(n * lg n)
#
# amortised: only invoked once
#
# space: O(n) since in top step the entire list is copied
#
# note: 
#  - because of the use of recursion, we might exhaust the stack; however, this seems to happen only 
#    around depth 1000, which means the list must have length around 2**1000, ie astronomical
#
def _merge_sort_merge(list_to_sort, p, q, r):
	left = list_to_sort[p:q]
	right = list_to_sort[q:r+1]
	i = 0
	j = 0
	for k in xrange(p, r+1):
		if not i < len(left):
			# we have exhausted 'left' so the rest must be in 'right'
			list_to_sort[k] = right[j]
			j += 1
		elif not j < len(right):
			# we have exhausted 'right' so the rest must be in 'left'
			list_to_sort[k] = left[i]
			i += 1
		elif left[i] <= right[j]:
			list_to_sort[k] = left[i]
			i += 1
		else:
			list_to_sort[k] = right[j]
			j += 1


def merge_sort(list_to_sort, p=0, r=None):
	if r == None: r = len(list_to_sort) - 1
	if p < r:
		q = (p + r) // 2
		# sort left branch
		merge_sort(list_to_sort, p, q)
		# sort right branch
		merge_sort(list_to_sort, q+1, r)
		# merge the two sorted branches
		_merge_sort_merge(list_to_sort, p, q+1, r)










#
# best case: O(n**2)
#
# worst case: O(n**2)
#
# average case: O(n**2)
#
# amortised: only invoked once
#
def bubble_sort(list_to_sort):
	for i in xrange(len(list_to_sort)):
		for j in xrange(len(list_to_sort) - 1, i, -1):
			if list_to_sort[j] < list_to_sort[j - 1]:
				temp = list_to_sort[j]
				list_to_sort[j] = list_to_sort[j - 1]
				list_to_sort[j - 1] = temp


#
# best case: O(n)
#
def bubble_sort_optimised(list_to_sort):
	for i in xrange(len(list_to_sort)):
		swapped = False
		for j in xrange(len(list_to_sort) - 1, i, -1):
			if list_to_sort[j] < list_to_sort[j - 1]:
				temp = list_to_sort[j]
				list_to_sort[j] = list_to_sort[j - 1]
				list_to_sort[j - 1] = temp
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
		print self._heap

	def print_tree(self, i=0, indent="", step="  "):
		if not i < self._heapsize: return
		print "{0}{1} [{2}]".format(indent, self._heap[i], i)
		self.print_tree(self.left(i), indent+step)
		self.print_tree(self.right(i), indent+step)
		
	# assuming heaps at left(i) and right(i) are max-heaps, turns heap at i into max-heap
	#  - worst-case running time is O(h) where h = ln n is height of tree rooted at i
	def max_heapify(self, i):
		print "max heapify"
		largest = i
		l = self.left(i)
		if l < self._heapsize and self._heap[l] > self._heap[i]: largest = l
		r = self.right(i)
		if r < self._heapsize and self._heap[r] > self._heap[largest]: largest = r
		if largest != i:
			# swap trick from stack overflow
			#  - supposedly works because Python first evaluates all of the right side
			self._heap[i], self._heap[largest] = self._heap[largest], self._heap[i]
			self.max_heapify(largest)
	
	# assuming heaps at left(i) and right(i) are min-heaps, turns heap at i into min-heap
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
			self._heap[i], self._heap[smallest] = self._heap[smallest], self._heap[i]
			self.min_heapify(smallest)
	
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
			
	def sort_max(self):
		self.build_max_heap()
		for i in xrange(len(self._heap)-1, 0, -1):
			# swap trick from stack overflow
			#  - supposedly works because Python first evaluates all of the right side
			self._heap[0], self._heap[i] = self._heap[i], self._heap[0]
			self._heapsize -= 1
			self.max_heapify(0)
			self.print_list()
			
	def sort_min(self):
		self.build_min_heap()
		# smallest element at root, so 
		for i in xrange(len(self._heap)-1, 0, -1):
			# swap trick from stack overflow
			#  - supposedly works because Python first evaluates all of the right side
			self._heap[0], self._heap[i] = self._heap[i], self._heap[0]
			self._heapsize -= 1
			self.min_heapify(0)


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

	
