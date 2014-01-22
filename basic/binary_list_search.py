

    

###################################
#
#  Binary search in sorted list
#
#
#  - the returned index is either the index of 'target' or where it fits best;
#     - in the latter case this means that 'numbers' with 'numbers[index] = target' is still sorted
#     - note that this is NOT necessarily the closest match in the array: it may be either to the immediate left or right
#
#  - worst case: O(lg n)
#  - best case: O(1), when 'target' found as first middle
#  - average case: O(lg n)
#
#  - notes:
#     - assumes 'numbers' to be sorted in increasing order
#

def binary_list_search_recursive(numbers, target, lower=0, upper=None):
    if upper == None: upper = len(numbers) - 1
    if lower > upper:
        # searching empty array so cannot be found
        return lower
    elif lower == upper:
        # searching array of size one so just check there
        return lower
    else: # lower < upper
        middle = (lower + upper) // 2
        if target == numbers[middle]: 
            # we happened to find it, great
            return middle
        elif target < numbers[middle]:
            # look in left subarray (excluding middle)
            return binary_list_search_recursive(numbers, target, lower, middle-1)
        else: # numbers[middle] < target
            # look in right subarray (excluding middle)
            return binary_list_search_recursive(numbers, target, middle+1, upper)

def binary_list_search_iterative(numbers, target, lower=0, upper=None):
    if upper == None: upper = len(numbers) - 1
    # loop-invariant: 'target' fits in subarray 'numbers[lower..upper]'
    while lower < upper:
        middle = (lower + upper) // 2
        if target == numbers[middle]:
            # we happened to find it
            # we could just 'return middle' here, but to stay with the loop-invariant we instead do:
            lower = middle
            upper = middle
            # ... so that 'target' fits in the required subarray
            break
        elif target < numbers[middle]:
            # proceeding in (strict) left subarray
            #  - ok for loop-invariant since being sorted implies that all in 'numbers[middle+1..upper]' are bigger
            upper = middle - 1
        else:
            # proceeding in (strict) right subarray
            #  - ok for loop-invariant since being sorted implies that all in 'numbers[lower..middle-1]' are lower
            lower = middle + 1
    # we may not have found it, but 'lower' is now best candidate
    #  - if 'lower == upper' then subarray is just one element, numbers[lower]
    #  - if 'lower > upper' then subarray is empty:
    #     - (assume that method not called with stupid input)
    #     - since rounding down in computing 'middle', this may only occur after going left in a size-two subarray
    #     - in that case, 'lower' was not changed; and since we went left, it was also the best candidate
    return lower

# default implementation
binary_list_search = binary_list_search_iterative
            












###################################
#
#  Closest match in list
#
#
#  - the returned index is either the index of 'target' or its closest match in terms of absolute value
#
#  - worst case: O(lg n)
#  - best case: O(1)
#  - average case: O(lg n)
#
#  - notes:
#     - assumes 'numbers' to be sorted in increasing order
#

# assumes unique numbers (looks only at immediate left and right candidate)
def closest_match(numbers, target):
    # find first candidate
    candidate_one = binary_list_search_iterative(numbers, target)
    if target == numbers[candidate_one]: 
        # found target so just return its index
        return candidate_one
    # find second candidate
    if target < numbers[candidate_one]: 
        # immediate left is also candidate
        candidate_two = max(candidate_one - 1, 0) 
    else:
        # immediate right is also candidate
        candidate_two = min(candidate_one + 1, len(numbers)-1)
    # find the closest of the two candidates
    if abs(target - numbers[candidate_one]) < abs(target - numbers[candidate_two]): 
        return candidate_one
    else: 
        return candidate_two
    
# alternative for when numbers are not unique
def closest_match_alternative(numbers, target):
    # find first candidate 
    candidate_one = binary_list_search_iterative(numbers, target)
    if target == numbers[candidate_one]: 
        # found target so just return its index
        return candidate_one
    # find second candidate
    if target < numbers[candidate_one]:
        # look for second candidate on the left (if any)
        candidate_two = candidate_one
        while numbers[candidate_one] == numbers[candidate_two] and candidate_two > 0:
            candidate_two -= 1
    else:
        # look for second candidate on the right (if any)
        candidate_two = candidate_one
        while numbers[candidate_one] == numbers[candidate_two] and candidate_two < len(numbers) - 1:
            candidate_two += 1
    # find the closest of the two candidates
    if abs(target - numbers[candidate_one]) < abs(target - numbers[candidate_two]):
        return candidate_one
    else:
        return candidate_two








        

