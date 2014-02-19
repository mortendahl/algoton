







class BinaryTreeNode:
    
    # inheritance doesn't seem to work properly when using this (additional fields in sub not available)
    #__slots__ = ['key', 'data', 'left', 'right', 'parent']

    def __init__(self, left=None, right=None, parent=None): 
        self.parent = parent
        self.left = left
        self.right = right
        
    def __str__(self):
        return "BinaryTreeNode()"




class BinaryTree:

    def __init__(self, root=None):
        self.root = root

    def preorder_walk(self, function, node=None):
        if node is None: node = self.root
        function(node)
        if node.left is not None: self.preorder_walk(function, node.left)
        if node.right is not None: self.preorder_walk(function, node.right)

    def inorder_walk(self, function, node=None):
        if node is None: node = self.root
        if node.left is not None: self.inorder_walk(function, node.left)
        function(node)
        if node.right is not None: self.inorder_walk(function, node.right)

    def postorder_walk(self, function, node=None):
        if node is None: node = self.root
        if node.left is not None: self.postorder_walk(function, node.left)      
        if node.right is not None: self.postorder_walk(function, node.right)
        function(node)

    def print_tree(self, node=None, indent="", step="  "):
        if node is None: node = self.root
        print "{0}{1}".format(indent, node)
        if node.left is not None: self.print_tree(node.left, indent+step)
        if node.right is not None: self.print_tree(node.right, indent+step)














class BinarySearchTreeNode(BinaryTreeNode):
    
    def __init__(self, key, left=None, right=None, parent=None): 
        BinaryTreeNode.__init__(self, left, right, parent)
        self.key = key
        
    def __str__(self):
        return "{0}".format(self.key)



class BinarySearchTreeNodeWithData(BinarySearchTreeNode):
    
    def __init__(self, key, data=None, left=None, right=None, parent=None): 
        BinarySearchTreeNode.__init__(self, key, left, right, parent)
        self.data = data
        
    def __str__(self):
        return "{0} ({1})".format(self.key, self.data)




class BinarySearchTree(BinaryTree):

    def __init__(self, root=None):
        BinaryTree.__init__(self, root)

    def search(self, key, node=None):
        if node is None: node = self.root
        while node is not None:
            if key == node.key:
                return node
            elif key < node.key:
                node = node.left
            else:
                node = node.right
        return None

    def closest_match(self, key, node=None):
        if node is None: node = self.root
        closest = node
        while node is not None:
            if key == node.key:
                return node
            elif key < node.key:
                if abs(node.key - key) < abs(closest.key - key): closest = node
                node = node.left
            else:
                if abs(node.key - key) < abs(closest.key - key): closest = node
                node = node.right
        return closest

    def minimum(self, node=None):
        if node is None: node = self.root
        if node is None: return None  # empty tree
        while node.left is not None:
            node = node.left
        return node

    def maximum(self, node=None):
        if node is None: node = self.root
        if node is None: return None  # empty tree
        while node.right is not None:
            node = node.right
        return node

    def successor(self, node):
        if node is None: return None
        # if there is any tree on the right, return smallest from there
        if node.right is not None:
            return self.minimum(node.right)
        # else search towards the root
        parent = node.parent
        while parent is not None:
            if node is parent.left:
                # we came up from the left
                return parent
            else:
                # we came up from the right
                node, parent = parent, parent.parent
        return None

    def predecessor(self, node):
        if node is None: return None
        # if there is any tree on the left, return largest from there
        if node.left is not None:
            return self.maximum(node.left)
        # else search towards the root
        parent = node.parent
        while parent is not None:
            if node is parent.right:
                # we came up from the right
                return parent
            else:
                # we came up from the left
                node, parent = parent, parent.parent
        return None

    # assume that node.left and node.right are both None (inserting a tree may break binary search tree property)
    def insert(self, node):
        parent = None
        candidate = self.root  # records candidate location for new node
        # traverse until we find an empty location
        while candidate is not None:
            if node.key == candidate.key:
                # move down right
                #  - we could do other things here (move left, store in linked list, ...)
                parent, candidate = candidate, candidate.right
            elif node.key < candidate.key:
                # move down left
                parent, candidate = candidate, candidate.left
            else:
                # move down right
                parent, candidate = candidate, candidate.right
        node.parent = parent
        if parent is None:
            self.root = node
        else:
            if node.key < parent.key: 
                parent.left = node
            else:
                parent.right = node

    def delete(self, node):
        # determine which node to remove
        if node.left is None or node.right is None:
            # if zero or one child
            node_to_splice = node
        else:
            # if two children
            node_to_splice = self.successor(node)
            node.key = node_to_splice.key
            node.data = node_to_splice.data
        # remove node: update child
        if node_to_splice.left is not None:
            # left child exists (and maybe also right)
            node_child = node_to_splice.left
            node_child.parent = node_to_splice.parent
        elif node_to_splice.right is not None:
            # only right child exists
            node_child = node_to_splice.right
            node_child.parent = node_to_splice.parent
        else:
            # no childred
            node_child = None
        # remove node: update parent
        if node_to_splice.parent is None:
            self.root = node_child
        else:
            if node_to_splice is node_to_splice.parent.left:
                node_to_splice.parent.left = node_child
            else:
                node_to_splice.parent.right = node_child


def binary_search_tree_from_sorted_list(lst, lower=0, upper=None):
    if upper is None: upper = len(lst) - 1
    if lower > upper:
        # empty array
        return None
    elif lower == upper:
        # array of size one
        return BinarySearchTreeNode(lst[lower])
        #return BinarySearchTreeNodeWithData(lst[lower], None)
    else: # lower < upper
        middle = (lower + upper) // 2
        left = binary_search_tree_from_sorted_list(lst, lower, middle-1)
        right = binary_search_tree_from_sorted_list(lst, middle+1, upper)
        key = lst[middle]
        node = BinarySearchTreeNode(key, left, right)
        #node = BinarySearchTreeNodeWithData(key, None, left, right)
        if left is not None: left.parent = node
        if right is not None: right.parent = node
        return node

def sorted_list_from_binary_search_tree(tree):
    lst = []
    tree.inorder_walk(lambda node: lst.append(node.key))
    return lst


nodes = [1,2,5,6,7,8]
tree = BinarySearchTree(binary_search_tree_from_sorted_list(nodes))
tree.print_tree()
print sorted_list_from_binary_search_tree(tree)
print tree.search(3)
print tree.closest_match(3).key
















class RadixTreeNode(BinaryTreeNode):
    
    def __init__(self, symbol, stored=False, left=None, right=None, parent=None): 
        BinaryTreeNode.__init__(self, left, right, parent)
        self.symbol = symbol
        self.stored = stored
        
    def __str__(self):
        return "{0} ({1})".format(self.symbol, self.stored)
        
        
        
        
        
        
        

class Radix(BinaryTree):
    
    def __init__(self, root=None):
        BinaryTree.__init__(self, root)
        
    def search(self, binstr):
        node = self.root
        for b in binstr:
            if b == '0':
                # left
                if node.left is None: return False
                node = node.left
            else:  # assume b == 1
                # right
                if node.right is None: return False
                node = node.right
        return node.stored if node is not None else False

    def insert(self, binstr):
        if self.root is None: self.root = RadixTreeNode(symbol='e', stored=False)
        node = self.root
        for b in binstr:
            if b == '0':
                # left
                if node.left is None: node.left = RadixTreeNode(symbol=b, stored=False, parent=node)
                node = node.left
            else:  # assume b == 1
                # right
                if node.right is None: node.right = RadixTreeNode(symbol=b, stored=False, parent=node)
                node = node.right
        node.stored = True

    # assume that binstr is a string over {'0', '1'}
    def delete(self, binstr):
        if self.root is None: return
        node = self.root
        for b in binstr:
            if b == '0':
                # left
                if node.left is None: return
                node = node.left
            else:  # assume b == 1
                # right
                if node.right is None: return
                node = node.right
        if node.left is None and node.right is None:
            # remove node if no children
            if node.parent is not None:
                if node is node.parent.left:
                    node.parent.left = None
                else:
                    node.parent.right = None
        else:
            # keep but update
            node.stored = False

    def sorted_strings(self, node=None, path=""):        
        lst = []
        if node is None: node = self.root
        if node.stored: lst.append(path)
        if node.left is not None: lst.extend(self.sorted_strings(node.left, path+"0"))
        if node.right is not None: lst.extend(self.sorted_strings(node.right, path+"1"))
        return lst


r = Radix()
r.insert("0")
r.insert("011")
r.insert("10")
r.insert("100")
r.insert("1011")
r.print_tree()
print r.sorted_strings()













class OrderStatisticTreeNode(BinarySearchTreeNode):
    
    def __init__(self, key, size=1, left=None, right=None, parent=None): 
        BinarySearchTreeNode.__init__(self, key, left, right, parent)
        self.size = size
        
    def __str__(self):
        return "{0} ({1})".format(self.key, self.size)
        
        
class OrderStatisticTree(BinarySearchTree):
        
    def __init__(self, root=None):
        BinarySearchTree.__init__(self, root)
        
    def select(self, index, node=None):
        if node is None: node = self.root
        if node is None: return None  # empty tree
        current_index = node.left.size if node.left is not None else 0
        if index == current_index:
            return node
        elif index < current_index:
            if node.left is not None: return self.select(index, node.left)
            else: return None
        else:
            nodes_before = current_index + 1
            if node.right is not None: return self.select(index - nodes_before, node.right)
            else: return None
            
    def rank(self, node):
        rank = node.left.size if node.left is not None else 0
        #while node is not self.root:
        while node.parent is not None:
            if node is node.parent.right:
                rank += node.parent.left.size + 1 if node.parent.left is not None else 1
            node = node.parent
        return rank
            
    def insert(self, node):
        parent = None
        candidate = self.root  # records candidate location for new node
        # traverse until we find an empty location
        while candidate is not None:
            if node.key == candidate.key:
                # add one to size
                candidate.size += 1
                # move down right
                #  - we could do other things here (move left, store in linked list, ...)
                parent, candidate = candidate, candidate.right
            elif node.key < candidate.key:
                # add one to size
                candidate.size += 1
                # move down left
                parent, candidate = candidate, candidate.left
            else:
                # add one to size
                candidate.size += 1
                # move down right
                parent, candidate = candidate, candidate.right
        node.parent = parent
        if parent is None:
            self.root = node
        else:
            if node.key < parent.key: 
                parent.left = node
            else:
                parent.right = node
                
    def delete(self, node):
        # we cannot use the inherited delete as it doesn't maintain the size field
        raise NotImplementedError
        
        
#root = OrderStatisticTreeNode(2, 5)
#left = OrderStatisticTreeNode(0, 2)
#leftright = OrderStatisticTreeNode(1, 1)
#right = OrderStatisticTreeNode(4, 3)
#rightleft = OrderStatisticTreeNode(3, 1)
#rightright = OrderStatisticTreeNode(5, 1)
#root.left, left.parent = left, root
#root.right, right.parent = right, root
#left.right, leftright.parent = leftright, left
#right.left, rightleft.parent = rightleft, right
#right.right, rightright.parent = rightright, right
#os = OrderStatisticTree(root)
#nodes = [left, leftright, root, rightleft, right, rightright]
#for i,node in enumerate(nodes):
#    assert os.select(i) is nodes[i]
#    assert os.rank(node) is i
#    #assert os.select(os.rank(node)) is node
        
        
#os = OrderStatisticTree()
#os.insert(OrderStatisticTreeNode(1))
#os.insert(OrderStatisticTreeNode(0))
#os.insert(OrderStatisticTreeNode(2))
#os.insert(OrderStatisticTreeNode(3))
#os.insert(OrderStatisticTreeNode(4))
#os.print_tree()
#print os.select(0) is os.search(0)
#print os.select(1) is os.search(1)
#print os.select(2) is os.search(2)
#print os.select(3) is os.search(3)
#print os.select(4) is os.search(4)
#print os.select(5) is None