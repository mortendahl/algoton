

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
		
		
l = [5,2,4,6,7,1,3]
insertion_sort(l)
print l










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

l = [5,2,4,6,7,1,3]
merge_sort(l)
print l










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
		

def binary_search_mustbe_while(numbers, target, lower=0, upper=None):
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


def binary_search_shouldbe_while(numbers, target, lower=0, upper=None):
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


def closest_match(numbers, target):
	index = binary_search_shouldbe_while(numbers, target)
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
	