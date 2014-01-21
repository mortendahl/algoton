


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

