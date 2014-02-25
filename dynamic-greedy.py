


######################
#
#  Assembly-line scheduling (Cormen et al. section 15.1)
#
#  - dynamic programming
#
#
#  note:
#   - assume that e0 and e1 have been inlined in a0[0] and a1[0] respectively
#   - assume that x0 and x1 have been inlined in a0[-1] and a1[-1] respectively
#   - assume that len(a0) = len(a1) = len(t0)+1 = len(t1)+1
#

argmin = lambda v0, v1: 0 if v0 <= v1 else 1


#
#  naive recursive approach
#

def assembly_line_scheduling_naive(a_same, a_other, t_same, t_other, id_same, id_other, j=None):
    if j is None: j = len(a_same)-1
    if j == 0:
        # fartest path through station j=0 is just the time of that station
        return [id_same], a_same[0]
    else:
        # fartest path for going through station j>0 if coming from same line
        path_same, price_same   = assembly_line_scheduling_naive(a_same, a_other, t_same, t_other, id_same, id_other, j-1)
        price_same += a_same[j]
        # fartest path for going through station j>0 if coming from the other line
        path_other, price_other = assembly_line_scheduling_naive(a_other, a_same, t_other, t_same, id_other, id_same, j-1)
        price_other += t_other[j-1] + a_same[j]
        # determine which was fartest
        if price_same <= price_other:
            # coming from same line was fartest
            path_same.append(id_same)
            return (path_same, price_same)
        else:
            # coming from the other line was fartest
            path_other.append(id_same)
            return (path_other, price_other)


#
#  dynamic programming approach
#

def assembly_line_scheduling_dynamic(a0, a1, t0, t1):
    n = len(a0)  # by assumptions, len(a0) == len(a1)
    f0 = [0]*n
    f1 = [0]*n
    l0 = [0]*n
    l1 = [0]*n
    f0[0] = a0[0]  # includes e1
    f1[0] = a1[0]  # includes e2
    l0[0] = 0
    l1[0] = 1
    for j in xrange(1,n):
        # time if going through station on line 0
        f0[j] =    min(f0[j-1] + a0[j], f1[j-1] + t1[j-1] + a0[j])
        l0[j] = argmin(f0[j-1] + a0[j], f1[j-1] + t1[j-1] + a0[j])
        # time if going through station on line 1
        f1[j] =    min(f0[j-1] + t0[j-1] + a1[j], f1[j-1] + a1[j])
        l1[j] = argmin(f0[j-1] + t0[j-1] + a1[j], f1[j-1] + a1[j])
    return f0, f1, l0, l1

def assembly_line_scheduling_dynamic_extract_way(l0, l1, choice):
    lst = []
    for next in reversed(zip(l0, l1)):
        lst.append(choice)
        choice = next[choice]
    lst.reverse()
    return lst


a0 = [7+2, 9, 3, 4, 8, 4+3]
a1 = [8+4, 5, 6, 4, 5, 7+2]
t0 = [2, 3, 1, 3, 4]
t1 = [2, 1, 2, 2, 1]

# naive approach
#path_same, price_same   = assembly_line_scheduling_naive(a0, a1, t0, t1, 0, 1)
#path_other, price_other = assembly_line_scheduling_naive(a1, a0, t1, t0, 1, 0)
#if price_same <= price_other: print path_same 
#else: print path_other

# dynamic programming approach
#f0, f1, l0, l1 = assembly_line_scheduling_dynamic(a0, a1, t0, t1)
#print assembly_line_scheduling_dynamic_extract_way(l0, l1, argmin(f0[-1], f1[-1]))














######################
#
#  Word split
#
#  - dynamic programming
#
#
#  note: 
#   - see also http://stackoverflow.com/questions/3466972/
#

def word_split_dynamic(str_to_split, words):
    # initialise array storing if it's possible to split sub-string str_to_split[:i+1]
    split_is_possible = [False]*len(str_to_split)
    # initialise array storing the word that made a split possible (or None if not)
    split_word = [None]*len(str_to_split)
    # bottom-up solving of subproblems
    for i in xrange(0, len(str_to_split)):
        # consider whole sub-word
        whole_word = str_to_split[:i+1]
        if whole_word in words: 
            # a split is possible if it is a word by itself
            split_is_possible[i] = True
            split_word[i] = whole_word
        else:
            # .. and if it is not a word by itself, try its subsub-words
            for j in range(i,0,-1):
                #left = str_to_split[0:j]
                right = str_to_split[j:i+1]
                if right in words and split_is_possible[j-1]: 
                    split_word[i] = right
                    split_is_possible[i] = True
    # test if it was possible to spil all the way up to the entire string
    if split_is_possible[-1]:
        # a split of the entire string is possible; extract words than made it possible
        str_words = []
        i = len(str_to_split)-1
        while i >= 0:
            cur = split_word[i]
            str_words.append(cur)
            i -= len(cur)
        str_words.reverse()
        return str_words
    else:
        # it was not possible to split the entire string
        return None

#print word_split_dynamic("house", set(["car", "carrot", "house"]))
#print word_split_dynamic("carrothouse", set(["car", "carrot", "house"]))
#print word_split_dynamic("carrothouses", set(["car", "carrot", "house"]))
#print word_split_dynamic("stringintowords", set(["string", "ring", "in", "to", "into", "words"]))
#print word_split_dynamic("finestring", set(["fine", "ring", "string"]))
#print word_split_dynamic("iseeyourattachment", set(["i", "see", "you", "your", "rat", "at", "attachment"]))


def word_split_naive(str_to_split, words):
    # consider whole word
    if str_to_split in words: 
        # a split is possible if it is a word by itself
        return [str_to_split]
    else:
        # .. and if it is not a word by itself, try its sub-strings
        for i in xrange(len(str_to_split)-1, -1, -1):
            left = str_to_split[:i]
            right = str_to_split[i:]
            if right in words: 
                str_words = word_split_naive(left, words)
                if str_words is not None:
                    # a split of left was possible; add right and return
                    str_words.append(right)
                    return str_words
        # it was not possible to split any sub-string
        return None
            
#print word_split_naive("house", set(["car", "carrot", "house"]))
#print word_split_naive("carrothouse", set(["car", "carrot", "house"]))
#print word_split_naive("carrothouses", set(["car", "carrot", "house"]))
#print word_split_naive("stringintowords", set(["string", "ring", "in", "to", "into", "words"]))
#print word_split_naive("finestring", set(["fine", "ring", "string"]))
#print word_split_naive("iseeyourattachment", set(["i", "see", "you", "your", "rat", "at", "attachment"]))














######################
#
#  Longest-common subsequence (Cormen et al. section 15.4)
#
#  - dynamic programming
#

def lcs_naive(strX, strY):
    if len(strX) == 0 or len(strY) == 0: return ""
    if strX[-1] == strY[-1]:
        # last character match
        sub_lcs = lcs_naive(strX[:-1], strY[:-1])
        return sub_lcs + strX[-1]
    else:
        # last character mis-match
        sub_lcs_1 = lcs_naive(strX[:-1], strY)
        sub_lcs_2 = lcs_naive(strX, strY[:-1])
        if len(sub_lcs_1) >= len(sub_lcs_2):
            return sub_lcs_1
        else:
            return sub_lcs_2
            
print lcs_naive("abcbdab", "bdcaba")
print lcs_naive("010110110", "10010101")


#def print_matrix(matrix):
#    for row in matrix:
#        print row

def lcs_dynamic(strX, strY):
    store = [[ 0 for col in range(len(strY)+1)] for row in range(len(strX)+1)]
    path  = [["" for col in range(len(strY)+1)] for row in range(len(strX)+1)]
    for ix in xrange(1, len(strX)+1):
        for iy in xrange(1, len(strY)+1):
            if strX[ix-1] == strY[iy-1]:
                # last character match
                store[ix][iy] = store[ix-1][iy-1] + 1
                path[ix][iy] = "d"  # diagonal
            else:
                # last character mis-match
                #store[ix][iy] = max(store[ix-1][iy], store[ix][iy-1])
                if store[ix-1][iy] >= store[ix][iy-1]:
                    store[ix][iy] = store[ix-1][iy]
                    path[ix][iy] = "u"  # up
                else:
                    store[ix][iy] = store[ix][iy-1]
                    path[ix][iy] = "l"  # left
    # extract path
    ix = len(strX)
    iy = len(strY)
    lcs = ""
    while ix > 0 and iy > 0:
        if path[ix][iy] == "d":
            lcs = strX[ix-1] + lcs
            ix -= 1
            iy -= 1
        elif path[ix][iy] == "l":
            iy -= 1
        else:
            ix -= 1
    return lcs

print lcs_dynamic("abcbdab", "bdcaba")
print lcs_dynamic("010110110", "10010101")














######################
#
#  Activity-selection (Cormen et al. section 16.1)
#
#  - greedy algorithm
#





######################
#
#  0-1 Knapsack (Cormen et al. section 16.3)