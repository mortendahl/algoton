


#
# best case: O(n)
#
# worst case: O(n)
#
# average case: O(n)
#

# assumes 'numbers' to be sorted in increasing order
def subset2_sum(numbers, target):
    merge_sort(numbers)   # sorted in-place
    lower = 0
    upper = len(numbers) - 1
    while lower < upper:
        current = numbers[lower] + numbers[upper]
        if target == current:
            # found solution
            return numbers[lower], numbers[upper]
        elif target > current:
            # move 'lower' up
            lower += 1
        elif target < current:
            # move 'upper' down
            upper -= 1
    return None

