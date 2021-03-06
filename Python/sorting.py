

#####################
#
#  Insertion sort 
#
#
#  - Cormen et al. p15-27
#
#  - example:
#     - j=1, key=4, i=0: [2,4,1,3] -> [2,4,1,3]
#     - j=2, key=1, i=1: -> [2,4,4,3], i=0: -> [2,2,4,3], i=-1: -> [1,2,4,3]
#     - j=3, key=3, i=2: -> [1,2,4,4], i=1: -> [1,2,3,4]
#
#  - worst case: O(n**2), when already sorted in decreasing order all elements willl be shifted
#  - best case: O(n), when already sorted so no shifting
#  - average case: half of worst case, since for each element half will be higher so half will be shifted
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

def merge_sort(numbers, p=0, r=None):
    if r is None: r = len(numbers) - 1
    if p < r:
        q = (p + r) // 2
        # sort left branch
        merge_sort(numbers, p, q)
        # sort right branch
        merge_sort(numbers, q+1, r)
        # merge the two sorted branches
        _merge_sort_merge(numbers, p, q+1, r)

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
#  - average case: O(n**2), since nothing makes it stop prematurely
#  - space: in-place
#

def bubble_sort(numbers):
    # loop-invariant: sub-array numbers[0..i] contains the i+1 smallest numbers, sorted increasingly
    for i in xrange(len(numbers)-1):
        # loop-invariant: numbers[j-1] smaller than all numbers in sub-array numbers[j..]
        for j in xrange(len(numbers)-1, i, -1):
            if numbers[j] < numbers[j-1]:
                # swap
                temp = numbers[j]
                numbers[j] = numbers[j-1]
                numbers[j - 1] = temp

#
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
            if numbers[j] < numbers[j-1]:
                # swap
                temp = numbers[j]
                numbers[j] = numbers[j-1]
                numbers[j - 1] = temp
                swapped = True
        if not swapped: return














#####################
#
#  Heap sort
#
#
#  - Cormen et al., section 6.4
#
#  - see MaxHeap.sort_increasing()
#
#  - worst case: O(n * lg n)
#  - best case: O(n * lg n)
#  - average case: O(n * lg n)
#  - space: in-place
#

from heap import MaxHeap

def heap_sort(numbers):
    heap = MaxHeap(numbers)
    heap.sort_increasing()
















#####################
#
#  Quick sort
#
#
#  - Cormen et al., section 7.......
#

def quick_sort(quick_sort_partition, numbers, p=0, r=None):
    if r is None: r = len(numbers)-1
    if p < r:
        q = quick_sort_partition(numbers, p, r)
        print p, q, r, "  --  ", q-p, r-q
        quick_sort(quick_sort_partition, numbers, p, q-1)
        quick_sort(quick_sort_partition, numbers, q+1, r)
        
#
#  randomised version
#

import random

def quick_sort_randomised(quick_sort_partition, numbers, p=0, r=None):
    if r is None: r = len(numbers)-1
    if p < r:
        # pick random integer from [p..r] (both inclusive)
        i = random.randint(p, r)
        # let this be the pivot position
        numbers[r], numbers[i] = numbers[i], numbers[r]
        # partition as in deterministic version
        q = quick_sort_partition(numbers, p, r)
        quick_sort_randomised(quick_sort_partition, numbers, p, q-1)
        quick_sort_randomised(quick_sort_partition, numbers, q+1, r)
        
#
#  semi-iterative version
#
#   - not completely tail recursive, but by recursing only on smaller 
#     partition we can limit stack size to O(lg n)
#   - we could do the same for the randomised version
#

def quick_sort_iterative(quick_sort_partition, numbers, p=0, r=None):
    if r is None: r = len(numbers)-1
    while p < r:
        q = quick_sort_partition(numbers, p, r)
        # assume that p <= q <= r (satisfied by Lomuto's partitioning)
        if q-p < r-q:
            # left partition is smallest
            quick_sort_iterative(quick_sort_partition, numbers, p, q-1)
            p = q+1
        else:
            # right partition is smallest
            quick_sort_iterative(quick_sort_partition, numbers, q+1, r)
            r = q-1

#
#  Lomuto's partitioning
#
#  - worst case: O(n**2)
#  - best case: O(n * lg n)
#  - average case: O(n * lg n)
#  - space: in-place
#
#  - example, numbers=[3,9,7,6,1,4], p=0, r=5:
#     - x=4, i=-1, j=0 -> [3,9,7,6,1,4], i=0
#                  j=1 -> [3,9,7,6,1,4], i=0
#                  j=2 -> [3,9,7,6,1,4], i=0
#                  j=3 -> [3,9,7,6,1,4], i=0
#                  j=4 -> [3,1,7,6,9,4], i=1
#                      -> [3,1,4,6,9,7]
#
#  - example, numbers[1,3,4,6,9,7], p=3, r=5:
#     - x=7, i=2, j=3 -> [1,3,4,6,9,7], i=3
#                 j=4 -> [1,3,4,6,9,7], i=3
#                     -> [1,3,4,6,7,9]
#

def quick_sort_partition_lomuto(numbers, p, r):
    x = numbers[r]  # pivot
    i = p - 1
    # loop-invariant: numbers[p..i] <= x < numbers[i+1..j-1]
    for j in xrange(p, r):
        if numbers[j] <= x:
            i += 1
            numbers[i], numbers[j] = numbers[j], numbers[i]
    numbers[i+1], numbers[r] = numbers[r], numbers[i+1]
    return i+1

quick_sort_lomuto = lambda numbers: quick_sort(quick_sort_partition_lomuto, numbers)

quick_sort_lomuto_randomised = lambda numbers: quick_sort_randomised(quick_sort_partition_lomuto, numbers)

quick_sort_lomuto_iterative = lambda numbers: quick_sort_iterative(quick_sort_partition_lomuto, numbers)














#####################
#
#  Counting sort
#
#
#  - Cormen et al., section 8.2.......
#
#
#  - worst case: O(n)
#  - best case: O(n)
#  - average case: O(n)
#  - space: O(n)
#

# assumes that all numbers are non-negative and no larger than max_number
def counting_sort(numbers, max_number=None):
    if max_number is None: max_number = max(numbers)
    # count numbers
    count = [0]*(max_number+1)
    for n in numbers: count[n] += 1
    # update count to positions
    for i in xrange(1, max_number+1): count[i] = count[i-1] + count[i]
    # write out result
    result = [0]*len(numbers)
    for i in xrange(len(numbers)-1, -1, -1):
        pos = count[numbers[i]] - 1
        count[numbers[i]] -= 1
        result[pos] = numbers[i]
    # write back into input list
    for i,n in enumerate(result): numbers[i] = n













#####################
#
#  Bucket sort (using sub sorting algo)
#
#
#  - Cormen et al., section 8.4.......
#

import itertools

# assumes sub_sorting_algo to sort in-place
def bucket_sort(sub_sorting_algo, numbers, max_number=None, no_buckets=None):
    if max_number is None: max_number = max(numbers)
    if no_buckets is None: no_buckets = len(numbers) / 3 # expect three numbers in each bucket
    factor = max_number / float(no_buckets-1)
    # initialise buckets
    buckets = [None]*no_buckets
    for bucket in xrange(no_buckets): buckets[bucket] = []
    # partition numbers into buckets
    for n in numbers:
        bucket = int(n/factor)
        buckets[bucket].append(n)
    # sort each bucket
    for bucket in xrange(no_buckets): sub_sorting_algo(buckets[bucket])
    # write back into input list
    sorted_numbers = (number for bucket in buckets for number in bucket)
    for i,n in enumerate(sorted_numbers): numbers[i] = n

#
#  using insertion_sort for sub-sorting:
#
#  - worst case: O(n**2)
#  - best case: O(n)
#  - average case: O(n)
#  - space: O(n)
#

bucket_sort_insertion_sort = lambda numbers: bucket_sort(insertion_sort, numbers)

#
#  using merge_sort for sub-sorting:
#
#  - worst case: O(n * lg n)
#  - best case: O(n)
#  - average case: O(n)
#  - space: O(n)
#
#  - notes:
#     - likely to still be worse than using insertion_sort when the buckets are small
#

bucket_sort_merge_sort = lambda numbers: bucket_sort(merge_sort, numbers)




















    

###################################
#
#  Binary search in sorted list
#
#
#  - the returned index is either the index of 'target' or where it fits best;
#     - in the latter case this means that 'numbers' with 'numbers[index] = target' is still sorted
#     - note that this is NOT necessarily the closest match in the array: it may be either to the immediate left or right
#
#  - worst case: O(lg n), when it has to visit a leaf
#  - best case: O(1), when 'target' found as first middle
#  - average case: O(lg n), half of worst case
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
#  - worst case: O(lg n), binary search + O(1)
#  - best case: O(1), binary search + O(1)
#  - average case: O(lg n), binary search + O(1)
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








        






###################################
#
#  Sub-set 2 sum
#
#
# best case: O(1)
#
# worst case: O(n)
#
# average case: O(n)
#

# assumes 'numbers' to be sorted in increasing order
def subset2_sum(numbers, target, lower=0, upper=None):
    if upper is None: upper = len(numbers)-1
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


###################################
#
#  Sub-set 3 sum
#
#
# best case: O(1)
#
# worst case: O(n**2)
#
# average case: O(n**2)
#

# assumes 'numbers' to be sorted in increasing order
def subset3_sum(numbers, target):
    for (i, x) in enumerate(numbers):
        sub_target = target - x
        sub_match = subset2_sum(numbers, sub_target, i+1)
        if sub_match is not None:
            (y,z) = sub_match
            return x,y,z
    return None
















#####################
#
#  Tests
#
        
if __name__ == '__main__':

    import random

    from timeit import Timer
    import gc




    def native_sort(numbers):
        numbers.sort()


    

    print "\n*** Tests, all algos ***\n"

    tests = [   random.sample(xrange(100000),    10),
                random.sample(xrange(100000),    50),
                random.sample(xrange(100000),   100),
                random.sample(xrange(100000),   500),
                random.sample(xrange(100000),  1000),
                random.sample(xrange(100000),  5000),
                random.sample(xrange(100000), 10000)   ]

    algos = [   #"quick_sort_lomuto",
                "quick_sort_lomuto_iterative",
                "bubble_sort",
                "bubble_sort_optimised",
                "insertion_sort",
                "heap_sort",
                "merge_sort",
                "quick_sort_lomuto_randomised",
                "counting_sort",
                "bucket_sort_merge_sort",
                "bucket_sort_insertion_sort",
                "native_sort"      ]

    for testlist in tests:
        for algoname in algos:
            # make a new copy of list since all algos override the input list
            listcopy = list(testlist)
            algocode = locals()[algoname]
            time = Timer(lambda: algocode(listcopy)).timeit(number=3)
            print "{0:<55} : {1:.10f}".format(algoname, time)
            gc.collect()
        print ""
        


    exit(0)
    


    print "\n*** Tests, fast algos ***\n"

    tests = [   random.sample(xrange(10000000),  20000),
                random.sample(xrange(10000000),  40000),
                random.sample(xrange(10000000), 100000),   ]

    algos = [   "heap_sort",
                "merge_sort",
                "quick_sort_lomuto_randomised",
                "counting_sort",
                "bucket_sort_insertion_sort",
                "native_sort"      ]

    for testlist in tests:
        for algoname in algos:
            # make a new copy of list since all algos override the input list
            listcopy = list(testlist)
            algocode = locals()[algoname]
            time = Timer(lambda: algocode(listcopy)).timeit(number=3)
            print "{0:<55} : {1:.10f}".format(algoname, time)
            gc.collect()
        print ""





