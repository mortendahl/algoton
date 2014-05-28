
from timeit import Timer
import gc









def k_combinations_recursive_bottomup(str, k):
    if len(str) < 1:
        return [""]
    else:
        char = str[0]
        combs = []
        if k < len(str):
            subcombs_excluding = k_combinations_recursive_bottomup(str[1:], k)
            for comb in subcombs_excluding:
                combs.append(comb)
        if k > 0:
            subcombs_including = k_combinations_recursive_bottomup(str[1:], k-1)
            for comb in subcombs_including:
                combs.append(char + comb)
        return combs
        
print k_combinations_recursive_bottomup("abcd", 0)
print k_combinations_recursive_bottomup("abcd", 1)
print k_combinations_recursive_bottomup("abcd", 2)
print k_combinations_recursive_bottomup("abcd", 3)
print k_combinations_recursive_bottomup("abcd", 4)



# useless?
def k_combinations_dynamic(str):
    k = len(str)
    store = [ [ list() for y in xrange(k+1) ] for x in xrange(len(str)+1) ]
    for row in store:
        row[0].append("")
    for irow in xrange(1, len(str)+1):
        for icol in xrange(1, k+1):
            for comb in store[irow-1][icol-1]:
                store[irow][icol].append(str[-irow] + comb)
            if icol < irow:
                for comb in store[irow-1][icol]:
                    store[irow][icol].append(comb)
    return store[-1]
            
print k_combinations_dynamic("abcde")
    








def k_combinations_recursive_topdown(str, k, f, output=""):
    if len(str) < 1:
        f(output)
        #acc.append(output)
    else:
        char = str[0]
        if k < len(str):
            k_combinations_recursive_topdown(str[1:], k, f, output)
        if k > 0:
            k_combinations_recursive_topdown(str[1:], k-1, f, output + char)



acc = []
k_combinations_recursive_topdown("abc", 0, lambda x: acc.append(x))
print acc
acc = []
k_combinations_recursive_topdown("abc", 1, lambda x: acc.append(x))
print acc
acc = []
k_combinations_recursive_topdown("abc", 2, lambda x: acc.append(x))
print acc
acc = []
k_combinations_recursive_topdown("abc", 3, lambda x: acc.append(x))
print acc









# considers the string as a set of characters and generates the powerset
#  - each recursion has two branches, resp. including and exclusing the front character
def combinations_recursive_bottomup(str):
    if len(str) < 1:
        # powerset of the empty set, is the empty set
        return [""]
    else:
        # extract front character
        char = str[0]
        # recursive compute combinations on substring
        combs = []
        # if char is excuded
        subcombs_excluding = combinations_recursive_bottomup(str[1:])
        for comb in subcombs_excluding:
            combs.append(comb)
        # if char is included
        subcombs_including = combinations_recursive_bottomup(str[1:])
        for comb in subcombs_including:
            combs.append(char + comb)
        return combs

#print combinations_recursive_bottomup("abc")
#print Timer(lambda: combinations_recursive_bottomup("a"*20)).timeit(number=3)
#gc.collect()




def combinations_recursive_bottomup_optimised_1(str):
    if len(str) < 1:
        # powerset of the empty set, is the empty set
        return [""]
    else:
        # extract front character
        char = str[0]
        # recursive compute combinations on substring
        subcombs = combinations_recursive_bottomup_optimised_1(str[1:])
        # combine with front character
        combs = []
        for comb in subcombs:
            combs.append(comb)
            combs.append(char + comb)
        return combs
print "foo"
print combinations_recursive_bottomup_optimised_1("abc")
print Timer(lambda: combinations_recursive_bottomup_optimised_1("a"*20)).timeit(number=3)
gc.collect()




def combinations_recursive_bottomup_optimised_2(str):
    if len(str) < 1:
        # powerset of the empty set, is the empty set
        return [""]
    else:
        # extract front character
        char = str[0]
        # recursive compute combinations on substring
        subcombs = combinations_recursive_bottomup_optimised_2(str[1:])
        # combine with front character
        old_length = len(subcombs)
        for i in xrange(old_length):
            subcombs.append(char + subcombs[i])
        return subcombs

#print combinations_recursive_bottomup_optimised_2("abc")
#print Timer(lambda: combinations_recursive_bottomup_optimised_2("a"*20)).timeit(number=3)
#gc.collect()




def combinations_recursive_topdown(str):
    acc = []
    combinations_recursive_topdown_helper(str, acc)
    return acc

def combinations_recursive_topdown_helper(str, acc, cur=""):
    if len(str) < 1:
        acc.append(cur)
    else:
        char = str[0]
        # excluded
        combinations_recursive_topdown_helper(str[1:], acc, cur)
        # included
        combinations_recursive_topdown_helper(str[1:], acc, cur + char)
        # result is now in acc

print combinations_recursive_topdown_helper("abc")
print Timer(lambda: combinations_recursive_topdown_helper("a"*20)).timeit(number=3)
gc.collect()




def combinations_iterative_righttoleft(str):
    # powerset of the empty set, is the empty set
    subcombs = [""]
    for char in reversed(str):
        old_length = len(subcombs)
        for i in xrange(old_length):
            subcombs.append(char + subcombs[i])
    return subcombs
    
#print combinations_iterative_righttoleft("abc")
#print Timer(lambda: combinations_iterative_righttoleft("a"*20)).timeit(number=3)
#gc.collect()




def combinations_iterative_lefttoright(str):
    # powerset of the empty set, is the empty set
    subcombs = [""]
    for char in str:
        old_length = len(subcombs)
        for i in xrange(old_length):
            subcombs.append(subcombs[i] + char)
    return subcombs
    
print combinations_iterative_lefttoright("abc")
print Timer(lambda: combinations_iterative_lefttoright("a"*20)).timeit(number=3)
gc.collect()















def permutations_recursive_topdown(str):
    acc = []
    permutations_recursive_topdown_helper(str, acc)
    return acc

def permutations_recursive_topdown_helper(str, acc, output=""):
    if len(str) < 1:
        acc.append(output)
    else:
        for i in xrange(len(str)):
            left = str[:i]
            char = str[i]
            right = str[i+1:]
            permutations_recursive_topdown_helper(left + right, acc, output + char)
    
print permutations_recursive_topdown("abc")
    
    
    