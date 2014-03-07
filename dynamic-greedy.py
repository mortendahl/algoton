


######################
#
#  Assembly-line scheduling (Cormen et al. section 15.1)
#
#   - find fastest path through two lines of stations
#
#
#  dynamic programming:
#   - problem can be broken down to finding fastest path through previous station on both lines
#   - by comparing the paths we get from extending each optimal sub-solution we may form a solution
#   - why is this solution optimal? 
#      - first, any optimal solution must be an extension of a sub-solution to the sub-problem
#        since a (fastest) path must go through a previous station on one of the two lines
#      - the used sub-solution must also be an optimal solution to the sub-problem since otherwise
#        we could cut-and-paste in an optimal sub-solution to get a better solution, contradicting
#        the fact that the solution is optimal
#      - then, since we considered the extensions of all optimal sub-solutions, we must have picked
#        an extension that was at least as good as any optimal solution
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
        # fastest path through station j=0 is just the time it takes to go through that station
        return [id_same], a_same[0]
    else:
        # fastest path for going through station j>0 if coming from same line
        path_same,  price_same  = assembly_line_scheduling_naive(a_same, a_other, t_same, t_other, id_same, id_other, j-1)
        price_same  += a_same[j]
        # fastest path for going through station j>0 if coming from the other line
        path_other, price_other = assembly_line_scheduling_naive(a_other, a_same, t_other, t_same, id_other, id_same, j-1)
        price_other += t_other[j-1] + a_same[j]
        # determine which was fastest
        if price_same <= price_other:
            # coming from same line was fastest
            path_same.append(id_same)
            return (path_same, price_same)
        else:
            # coming from the other line was fastest
            path_other.append(id_same)
            return (path_other, price_other)


#
#  dynamic programming (bottom-up) approach
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


#a0 = [7+2, 9, 3, 4, 8, 4+3]
#a1 = [8+4, 5, 6, 4, 5, 7+2]
#t0 = [2, 3, 1, 3, 4]
#t1 = [2, 1, 2, 2, 1]

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
#   - split string into a set of words, where optimal means None if no split is possible and no left-over characters otherwise
#
#
#  dynamic programming:
#   - problem can be broken down by removing a last word and finding an optimal split of remaining sub-string
#      - if there's no last word then no split is possible and hence returning None is optimal
#   - by comparing the solutions we get from extending each optimal sub-split we may form a solution
#   - why is this solution optimal?
#     - first, any optimal solution must remove a last word and give optimal split of remaining sub-string
#     - since we've compared all possible last words, we also considered the one used in the optimal solution,
#       and hence our solution is at least as optimal
#
#  note: 
#   - see also http://stackoverflow.com/questions/3466972/
#


#
#  naive approach
#

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


#
#  dynamic programming approach
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

















######################
#
#  Longest-common subsequence (Cormen et al. section 15.4)
#
#  - find longest common subsequence Z of two strings X and Y
#
#
#  dynamic programming:
#   - if X[-1] == Y[-1] then finding a LCS may be broken down by recursing on X[:-1] and Y[:-1]
#      - from an optimal sub-solution we may form a solution by appending X[-1] (or Y[-1])
#      - why is this an optimal solution?
#         - any optimal solution Z must end with X[-1] (or Y[-1]) since otherwise we could extend it;
#         - furthermore, Z[:-1] must be an optimal sub-solution to X[:-1] and Y[:-1] since o.w. contradiction by cut-and-paste
#         - since we used an optimal sub-solution, our solution must be at least as good
#   - if X[-1] != Y[-1] then finding a LCS may be broken down by recursing on X[:-1] and Y, or X and Y[:-1]
#      - from an optimal sub-solution we may form a solution (by doing nothing)
#      - why is this an optimal solution?
#         - any optimal solution Z must exclude either X[-1] or Y[-1] since they differ, hence Z is actually
#           an optimal sub-solution to one of the two sub-problems (otherwise cut-and-paste gives contradiction)
#         - since we compared the optimal sub-solution to both sub-problems we must have used one that is
#           at least as optimal as Z; and since Z is optimal our solution is optimal as well
#


#
#  naive recursive approach
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
            
#print lcs_naive("abcbdab", "bdcaba")
#print lcs_naive("010110110", "10010101")


#
#  dynamic programming approach
#

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

#print lcs_dynamic("abcbdab", "bdcaba")
#print lcs_dynamic("010110110", "10010101")














######################
#
#  0-1 Knapsack (Cormen et al. section 16.3)
#
#  - put items with highest total value in sack
#
#
#  dynamic programming:
#   - problem can be broken down by considering one less item for potential inclusion in the sack
#   - by comparing the optimal total value obtained by extending either the sub-problem where the last 
#     item (according to any ordering) was included (and hence less room for other items) or the 
#     sub-problem where the last item was not included, we find a solution
#   - why is this an optimal solution?
#      - an optimal solution must decide to either include the item or not
#      - and in either case, the optimal solution must be an extension of an optimal sub-solution (o.w. cut-and-paste ...)
#      - but we compared the extension of all optimal sub-solutions and hence our solution is at least as optimal
#


#
#  naive recursive approach
#

def knapsack_naive(items, remaining_weight):
    if len(items) == 0: return 0  # no (more) items to consider, so total value is 0
    item = items[0]  # pick item to consider for inclusion/exclusion
    item_weight = item[0]
    item_value  = item[1]
    if item_weight <= remaining_weight:
        # it's possible to include the item
        # if we include it we get:
        total_value_if_included = knapsack_naive(items[1:], remaining_weight - item_weight) + item_value
        # .. and if we don't we get:
        total_value_if_excluded = knapsack_naive(items[1:], remaining_weight)
        return max(total_value_if_included, total_value_if_excluded)
    else:
        # item weights too much, can't include it
        return knapsack_naive(items[1:], remaining_weight)


#
#  dynamic programming approach
#

def knapsack_dynamic(items, total_remaining_weight):
    # first row is when there is no remaining_weight; 
    # first column is when there are no items left
    # .. in both cases do we have a value of 0
    store = [[ 0 for col in range(len(items)+1)] for row in range(total_remaining_weight+1)]    
    for i,item in enumerate(items):
        item_weight = item[0]
        item_value  = item[1]
        for remaining_weight in range(1, total_remaining_weight+1):
            if item_weight <= remaining_weight:
                value_if_included = store[remaining_weight - item_weight][i] + item_value
                value_if_excluded = store[remaining_weight][i]
                store[remaining_weight][i+1] = max(value_if_included, value_if_excluded)
            else:
                value_if_excluded = store[remaining_weight][i]
                store[remaining_weight][i+1] = value_if_excluded
    #for i,row in enumerate(store):
    #    print i,row
    return store[total_remaining_weight][len(items)]


#items = [ (10, 60), (20, 100), (30, 120) ]  # (weight, value)
#print knapsack_naive(items, 50)
#print knapsack_dynamic(items, 50)

















######################
#
#  Checker board (Cormen et al. section 16.1)
#
#  - move from bottom row to top row, moving either straight up, diagonally up left, 
#    or diagonally up right (when possible), collection as much as possible
#
#
#  dynamic programming:
#   - from a field we can break the problem down till at most three sub-problems (up, left, and, right)
#   - we can find a field's value by comparing the extensions of optimal sub-solutions
#   - why is this an optimal solution:
#     - an optimal solution must pick one of the moves we considered, and must find an optimal value of the sub-fields;
#       if it didn't we could make a better move and get a better field value, contradicting optimality
#     - hence since we consider the same moves we compare the same extensions when forming our solution
#       and so it must be at least as optimal
#


#
#  naive recursive approach
#
        
def checkerboard_naive(board, irow, icol):
    if irow == 0: 
        # at top; collect only what's at that field
        return board[irow][icol]
    else:
        move_values = []
        # we can always move straight up (since irow != 0)
        move_up_value = board[irow][icol] + checkerboard_naive(board, irow-1, icol)
        move_values.append(move_up_value)
        # we can move to the left if not at left border
        if icol > 0:
            move_left_value = board[irow][icol] + checkerboard_naive(board, irow-1, icol-1) 
            move_values.append(move_left_value)
        # we can move to the right if not at right border
        if icol < len(board[irow])-1:
            move_right_value = board[irow][icol] + checkerboard_naive(board, irow-1, icol+1)
            move_values.append(move_right_value)
        return max(move_values)
        

#
#  dynamic programming approach
#

def checkerboard_dynamic(board):
    store = [ [0 for col in row] for row in board ]
    # build first row of store (copy from board since no moves are possible)
    irow = 0
    for icol in xrange(len(board[irow])):
        store[irow][icol] = board[irow][icol]
    #print "  "
    #for row in store:
    #    print row
    # build rest of the rows of store
    for irow in xrange(1, len(board)):
        for icol in xrange(len(board[irow])):
            move_values = []
            # we can always move straight up (since irow != 0)
            move_up_value = board[irow][icol] + store[irow-1][icol]
            move_values.append(move_up_value)
            # we can move to the left if not at left border
            if icol > 0:
                move_left_value = board[irow][icol] + store[irow-1][icol-1]
                move_values.append(move_left_value)
            # we can move to the right if not at right border
            if icol < len(board[irow])-1:
                move_right_value = board[irow][icol] + store[irow-1][icol+1]
                move_values.append(move_right_value)
            store[irow][icol] = max(move_values)
        #print "  "
        #for row in store:
        #    print row
    return max(store[-1])

       
#board = [  [  1,  2,  3,  4,  5 ],
#           [ -1, -2, -3, -4, -5 ],
#           [  5,  4,  3,  2,  1 ],
#           [ -5, -4, -3, -2, -1 ],
#           [  1,  2,  3,  4,  5 ]  ]
#
#print max([checkerboard_naive(board, len(board)-1, icol) for icol in xrange(len(board[0]))])
#print checkerboard_dynamic(board)

















######################
#
#  Scheduling to maximize profit (Cormen et al. problem 15-7 p. 369)
#
#
#  dynamic programming
#
















######################
#
#  Activity-selection (Cormen et al. section 16.1)
#
#  - greedy algorithm
#


# use lists to characterise problems (look for max number of compatible activities in list)
# any ordering works
#  - unclear how to fill out tableau for dynamic programming solution (lacking simple structure in sub-problem formulation)
def activity_selection_naive_sublists(activities):
    # consider each activity
    choices = [0]  # as a default value we can fit 0 activities
    for activity_index,activity in enumerate(activities):
        # divide the remaining activities into those that are compatible because they end before
        activities_before = filter(lambda other_activity: other_activity[1] < activity[0], activities)
        # .. and those that are compatible because they end after
        activities_after  = filter(lambda other_activity: activity[1] <= other_activity[0], activities)
        # and get maximum from recursion
        max_activities_before = activity_selection_naive_sublists(activities_before)
        max_activities_after  = activity_selection_naive_sublists(activities_after)
        choices.append(max_activities_before + 1 + max_activities_after)
    return max(choices)

# re-use activities list for each recursive call, but limit by interval instead
# use intervals to characterise problems (look for max number of compatible activities fitting in interval)
# any ordering works
#  - allows easy method for filling out tableau for dynamic programming solution, yet pseudo-polynomial
def activity_selection_naive_interval(activities, interval_start=None, interval_finish=None):
    # initialise for root case
    if interval_start is None: interval_start = 0
    if interval_finish is None: interval_finish = max(map(lambda (x,y): y, activities))+1  # one more than the latest
    # consider each activity
    choices = [0]  # as a default value we can fit 0 activities
    for activity in activities:
        activity_start  = activity[0]
        activity_finish = activity[1]
        if interval_start <= activity_start and activity_finish < interval_finish:
            # activity is compatible with interval
            # find maximum number of activities that can fit in before
            max_activities_before = activity_selection_naive_interval(activities, interval_start, activity_start)
            # .. and after this activity
            max_activities_after  = activity_selection_naive_interval(activities, activity_finish, interval_finish)
            choices.append(max_activities_before + 1 + max_activities_after)
    return max(choices)
    
# re-use activities list for each recursive call, but limit by index instead
# use indices to characterise intervals and in turn problems (look for max number of activities that fits before and after)
# any ordering works
#  - unclear how to fill out tableau for dynamic programming solution (lacking simple structure in sub-problem formulation)
#  - problem is to guarantee that the right values are in the tableau when we need them
def activity_selection_naive_indices(activities, index_before_activity=None, index_after_activity=None):
    # initialise for root case
    if index_before_activity is None: 
        activities = [(-2,-1)] + activities
        index_before_activity = 0
    if index_after_activity is None: 
        max_finishing_time = max(map(lambda (x,y): y, activities))
        activities = activities + [(max_finishing_time+1,max_finishing_time+2)]
        index_after_activity = len(activities)-1
    # consider each activity
    choices = [0]  # as default value we can fit 0 activities
    for index_activity in xrange(0, len(activities)):
        activity = activities[index_activity]
        if activities[index_before_activity][1] <= activity[0] and activity[1] < activities[index_after_activity][0]:
            # activity is compatible with interval
            # find activities before
            max_activities_before = activity_selection_naive_indices(activities, index_before_activity, index_activity)
            # .. and after
            max_activities_after  = activity_selection_naive_indices(activities, index_activity, index_after_activity)
            choices.append(max_activities_before + 1 + max_activities_after)
    return max(choices)

# re-use activities list for each recursive call, but limit by index instead
# use indices to characterise intervals and in turn problems (look for max number of activities that fits before and after)
# assume sorted order so that at each level we already have a limit on the candidates
#  - allows easy method for filling out tableau for dynamic programming solution, polynomial
def activity_selection_naive_indices_sorted(activities, index_before_activity=None, index_after_activity=None):
    # initialise for root case
    if index_before_activity is None: 
        activities = [(-2,-1)] + activities
        index_before_activity = 0
    if index_after_activity is None: 
        max_finishing_time = max(map(lambda (x,y): y, activities))
        activities = activities + [(max_finishing_time+1,max_finishing_time+2)]
        index_after_activity = len(activities)-1
    # consider each activity
    choices = [0]  # as default value we can fit 0 activities
    for index_activity in xrange(index_before_activity, index_after_activity):
        activity = activities[index_activity]
        if activities[index_before_activity][1] <= activity[0] and activity[1] < activities[index_after_activity][0]:
            # activity is compatible with interval
            # find activities before
            max_activities_before = activity_selection_naive_indices_sorted(activities, index_before_activity, index_activity)
            # .. and after
            max_activities_after  = activity_selection_naive_indices_sorted(activities, index_activity, index_after_activity)
            choices.append(max_activities_before + 1 + max_activities_after)
    return max(choices)

def activity_selection_dynamic_indices_sorted(activities):
    # append dummy activities
    min_starting_time =  min(map(lambda (x,y): x, activities))
    max_finishing_time = max(map(lambda (x,y): y, activities))
    activities = [(min_starting_time-2, min_starting_time-1)] + activities + [(max_finishing_time+1, max_finishing_time+2)]
    # initialise tableau
    n = len(activities)  # including extra lower and upper activity
    tableau = [ [ 0 for icol in xrange(n) ] for irow in xrange(n) ]
    # fill rest of tableau bottom-up
    for index_before_activity in xrange(n-1-2, -1, -1):
        for index_after_activity in xrange(index_before_activity+2, n):
            choices = [0]
            for index_activity in xrange(index_before_activity, index_after_activity):
                activity = activities[index_activity]
                if activities[index_before_activity][1] <= activity[0] and activity[1] < activities[index_after_activity][0]:
                    # find activities before
                    max_activities_before = tableau[index_before_activity][index_activity]
                    # .. and after
                    max_activities_after  = tableau[index_activity][index_after_activity]
                    choices.append(max_activities_before + 1 + max_activities_after)
            tableau[index_before_activity][index_after_activity] = max(choices)
    return tableau[0][n-1]

def activity_selection_greedy_indices_sorted(activities):
    if len(activities) < 1: return len([])
    current = activities[0]
    selection = [current]
    for activity in activities[1:]:
        if current[1] <= activity[0]:
            # include activity
            selection.append(activity)
            current = activity
    return len(selection)
        

activities = [ (8,12), (1,4), (3,8), (3,5), (0,6), (12,14), (5,7), (6,10), (5,9), (8,11), (2,13) ]  # (start_time, finish_time)
print activity_selection_naive_sublists(activities)
print activity_selection_naive_interval(activities)
print activity_selection_naive_indices(activities)
print activity_selection_naive_indices_sorted(sorted(activities, key=lambda (x,y): y))
print activity_selection_dynamic_indices_sorted(sorted(activities, key=lambda (x,y): y))
print activity_selection_greedy_indices_sorted(sorted(activities, key=lambda (x,y): y))





