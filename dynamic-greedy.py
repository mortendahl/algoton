


######################
#
#  Assembly-line scheduling (Cormen et al. section 15.1)
#
#  - dynamic programming algorithm
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
path_same, price_same   = assembly_line_scheduling_naive(a0, a1, t0, t1, 0, 1)
path_other, price_other = assembly_line_scheduling_naive(a1, a0, t1, t0, 1, 0)
if price_same <= price_other: print path_same 
else: print path_other

# dynamic programming approach
f0, f1, l0, l1 = assembly_line_scheduling_dynamic(a0, a1, t0, t1)
print assembly_line_scheduling_dynamic_extract_way(l0, l1, argmin(f0[-1], f1[-1]))














######################
#
#  Word split
#
#  - dynamic programming algorithm
#









######################
#
#  Activity-selection (Cormen et al. section 16.1)
#
#  - greedy algorithm
#





######################
#
#  0-1 Knapsack (Cormen et al. section 16.3)