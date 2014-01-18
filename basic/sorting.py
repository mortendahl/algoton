

#
# best case: O(n), when already sorted so no shifting
#
# worst case: O(n**2), when already sorted in decreasing order all elements willl be shifted
#
# average case: half of worst case, since for each element, half will be higher so half will be shifted
#
# amortised: only invoked once
#
def insertion_sort(list_to_sort):
	for j in xrange(1, len(list_to_sort)):
		key = list_to_sort[j]
		i = j - 1
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
	if r == None: r = len(list_to_sort)-1
	if p < r:
		q = (p + r) // 2
		merge_sort(list_to_sort, p, q)
		merge_sort(list_to_sort, q+1, r)
		_merge_sort_merge(list_to_sort, p, q+1, r)

l = [5,2,4,6,7,1,3]
merge_sort(l)
print l
