







class TreeNode:
    
    __slots__ = ['key', 'data', 'left', 'right', 'parent']

    def __init__(self, key, data=None, left=None, right=None, parent=None): 
        self.key = key
        self.data = data
        self.parent = parent
        self.left = left
        self.right = right


def print_tree(node, indent="", step="  "):
    if node is None: return
    print "{0}{1} ({2})".format(indent, node.key, node.data)
    print_tree(node.left, indent+step)
    print_tree(node.right, indent+step)














class BinaryTree:

    def __init__(self, root=None):
        self.root = root

    def preorder_walk(self, function, node=None):
        if node is None: node = self.root
        function(node.key)
        if node.left is not None: self.preorder_walk(function, node.left)
        if node.right is not None: self.preorder_walk(function, node.right)

    def inorder_walk(self, function, node=None):
        if node is None: node = self.root
        if node.left is not None: self.inorder_walk(function, node.left)
        function(node.key)
        if node.right is not None: self.inorder_walk(function, node.right)

    def postorder_walk(self, function, node=None):
        if node is None: node = self.root
        if node.left is not None: self.postorder_walk(function, node.left)      
        if node.right is not None: self.postorder_walk(function, node.right)
        function(node.key)














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
        return TreeNode(*lst[lower])
    else: # lower < upper
        middle = (lower + upper) // 2
        left = binary_search_tree_from_sorted_list(lst, lower, middle-1)
        right = binary_search_tree_from_sorted_list(lst, middle+1, upper)
        key = lst[middle][0]
        data = lst[middle][1]
        node = TreeNode(key, data, left, right)
        if left is not None: left.parent = node
        if right is not None: right.parent = node
        return node

def sorted_list_from_binary_search_tree(tree):
    lst = []
    tree.inorder_walk(lambda x: lst.append(x))
    return lst


#nodes = [1,2,5,6,7,8]
#tree = BinarySearchTree(binary_search_tree_from_sorted_list(map(lambda i: (i,None), nodes)))
#print tree.closest_match(3).key














class Radix(BinaryTree):
    
    def __init__(self, root=None):
        self.root = root
        
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
        return node.data if node is not None else False

    def insert(self, binstr):
        if self.root is None: self.root = TreeNode('e', False)
        node = self.root
        for b in binstr:
            if b == '0':
                # left
                if node.left is None: node.left = TreeNode(b, False, parent=node)
                node = node.left
            else:  # assume b == 1
                # right
                if node.right is None: node.right = TreeNode(b, False, parent=node)
                node = node.right
        node.data = True

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
            node.data = False

    def sorted_strings(self, node=None, path=""):        
        lst = []
        if node is None: node = self.root
        if node.data == True: lst.append(path)
        if node.left is not None: lst.extend(self.sorted_strings(node.left, path+"0"))
        if node.right is not None: lst.extend(self.sorted_strings(node.right, path+"1"))
        return lst


#r = Radix()
#r.insert("0")
#r.insert("011")
#r.insert("10")
#r.insert("100")
#r.insert("1011")
#print r.sorted_strings()





