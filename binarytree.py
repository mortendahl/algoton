


class BinaryTreeNode:
    __slots__ = ['data', 'parent', 'left', 'right']

    def __init__(self, data, left=None, right=None, parent=None): 
        self.data = data
        self.parent = parent
        self.left = left
        self.right = right
    
    def print_tree(self, indent="", step="  "):
        print "{0}{1}".format(indent, self.data)
        if self.left is not None: self.left.print_tree(indent+step)
        if self.right is not None: self.right.print_tree(indent+step)
    
    def print_list(self):
        if self.left is not None: self.left.print_list()
        print self.data
        if self.right is not None: self.right.print_list()

    


def tree_from_list(lst, lower=0, upper=None):
    if upper is None: upper = len(lst) - 1
    if lower > upper:
        # empty array
        return None
    elif lower == upper:
        # array of size one
        return BinaryTreeNode(lst[lower])
    else: # lower < upper
        middle = (lower + upper) // 2
        left = tree_from_list(lst, lower, middle-1)
        right = tree_from_list(lst, middle+1, upper)
        node = BinaryTreeNode(lst[middle], left, right)
        if left is not None: left.parent = node
        if right is not None: right.parent = node
        return node



def tree_to_list(root):
    lst = []
    if root.left is not None: lst.extend(tree_to_list(root.left))
    lst.append(root.data)
    if root.right is not None: lst.extend(tree_to_list(root.right))
    return lst

        
        




# assumes the tree to be 'sorted' in increasing order
def binary_search(root, target):
    if target == root.data:
        return root
    else:
        if target < root.data:
            if root.left is None: return None
            return binary_search(root.left, target)
        else:
            if root.right is None: return None
            return binary_search(root.right, target)


# assumes the tree to be 'sorted' in increasing order
def closest_match(root, target, closest=None):
    if closest is None: closest = root
    # either we found it, or we pick left or right
    if target == root.data: return root
    elif target < root.data: candidate = root.left
    else: candidate = root.right
    # are we closer at this step?
    if abs(root.data - target) < abs(closest.data - target): closest = root
    # if at a leaf we return whatever was closest
    if candidate is None: return closest
    # .. otherwise we keep looking
    else: return closest_match(candidate, target, closest)


# assumes the tree to be 'sorted' in increasing order
def closest_match_alternative(root, target, closest=None):
    if closest is None: closest = root
    # either we found it, or we pick left or right
    if target == root.data: 
        return root
    else:
        # are we closer at this step?
        if abs(root.data - target) < abs(closest.data - target): closest = root
        # look left or right?
        if target < root.data: 
            if root.left is None: return closest
            return closest_match(root.left, target, closest)
        else: 
            if root.right is None: return closest
            return closest_match(root.right, target, closest)
        
            
            
#l1 = [1,2,3,4,5]
#t1 = tree_from_list(l1)
#t1.print_tree()


#l2 = [1,2,3,4,5,6,7,8]
#t2 = tree_from_list(l2)
#t2.print_tree()


l3 = [1,2,5,6,7,8]
t3 = tree_from_list(l3)
print closest_match(t3, 3).data