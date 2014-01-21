

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
#
#  - worst case: O(n * lg n)
#  - best case: O(n * lg n)
#  - average case: O(n * lg n)
#  - space: in-place
#

def quick_sort(numbers):
    pass
















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

    tests = [   random.sample(xrange(10000), 5000),
                random.sample(xrange(100000), 10000)   ]

    algos = [   "bubble_sort",
                "bubble_sort_optimised",
                "insertion_sort",
                "heap_sort",
                "merge_sort",
                "quick_sort",
                "native_sort"      ]

    for testlist in tests:
        for algoname in algos:
            # make a new copy of list since all algos override the input list
            listcopy = list(testlist)
            algocode = locals()[algoname]
            time = Timer(lambda: algocode(listcopy)).timeit(number=3)
            print "{0:<55} : {1}".format(algoname, time)
            gc.collect()
        print ""






    print "\n*** Tests, fast algos ***\n"

    tests = [   random.sample(xrange(1000000), 20000),
                random.sample(xrange(1000000), 40000),
                random.sample(xrange(10000000), 100000),   ]

    algos = [   "heap_sort",
                "merge_sort",
                "quick_sort",
                "native_sort"      ]

    for testlist in tests:
        for algoname in algos:
            # make a new copy of list since all algos override the input list
            listcopy = list(testlist)
            algocode = locals()[algoname]
            time = Timer(lambda: algocode(listcopy)).timeit(number=3)
            print "{0:<55} : {1}".format(algoname, time)
            gc.collect()
        print ""





