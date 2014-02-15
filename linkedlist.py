
#
# Functional alternative at http://stackoverflow.com/questions/280243/python-linked-list#280284
#




#
#  Singly linked-list using Python lists as nodes: [key, data, next] where data is satellite data
#
#
#  notes:
#   - uses special 'sentinal' node to indicate 'end of list'; sentinal[2] is head of list
#

class SinglyLinkedList:

    def __init__(self, lst=[]):
        # set-up special 'sentinal' node
        sentinal = [None, None, None]   # [key, data, next]
        sentinal[2] = sentinal
        self.sentinal = sentinal
        # add any items given (to comply with 'construct-as-printed' pattern)
        self.extend(lst)

    def _insert_node_head(self, node):
        # make node point to old head
        node[2] = self.sentinal[2]
        # make node head
        self.sentinal[2] = node
        
    def _insert_node_tail(self, node):
        # traverse list to find tail, ie node with next pointing to sentinal
        tail_node = self.sentinal
        while tail_node[2] is not self.sentinal:
            tail_node = tail_node[2]
        # make tail node point to new node
        tail_node[2] = node
        # make new node point back to sentinal
        node[2] = self.sentinal

    # assume that predicate does not match sentinal
    def _remove_first_node(self, predicate):
        # traverse list to find 'prev_node' pointing to 'node'
        prev_node = self.sentinal
        while prev_node[2] is not self.sentinal:
            node = prev_node[2]
            if predicate(node):
                # make prev_node before node in the chain point to the node after node
                prev_node[2] = node[2]
                return
            else:
                # move to next
                prev_node = prev_node[2]
    
    def _find_first_node(self, predicate):
        # traverse list
        node = self.sentinal[2]
        while node is not self.sentinal:
            if predicate(node): return node
            node = node[2]
        return None
                
    def insert_head(self, key, data):
        node = [key, data, None]
        self._insert_node_head(node)
        
    def insert_tail(self, key, data):
        node = [key, data, None]
        self._insert_node_tail(node)
                
    def remove_first(self, key):
        predicate = lambda node: True if node[0] == key else False
        self._remove_first_node(predicate)
        
    def remove_head(self):
        
        
    def find(self, key):
        predicate = lambda node: True if node[0] == key else False
        node = self._find_first_node(predicate)
        return node[1] if node is not None else None
        
    def head(self):
        node = self.sentinal[2]
        return (node[0], node[1]) if node is not self.sentinal else None
        
    def keys(self):
        # traverse list
        node = self.sentinal[2]
        while node is not self.sentinal:
            yield node[0]
            node = node[2]

    def extend(self, lst):
        for pair in reversed(lst):
            self.insert_head(*pair)

    def __str__(self):
        str = "SinglyLinkedList(["
        node = self.sentinal[2]
        if node is not self.sentinal:
            str += "({0},{1})".format(node[0], node[1])
            node = node[2]
        while node is not self.sentinal:
            str += ", ({0},{1})".format(node[0], node[1])
            node = node[2]
        return str + "])"

    def print_chain(self):
        node = self.sentinal[2]
        while node is not self.sentinal:
            print "{0} {1} ".format(node[0], "->" if node[2] is not self.sentinal else "  ")
            node = node[2]


sl = SinglyLinkedList()
for n in xrange(5,0,-1):
    sl.insert_head(n, n*10)
    print sl
for m in xrange(6,11):
    sl.insert_tail(m, m*10)
    print sl






class Stack:

    def __init__(self, lst=[]):
        self._linkedlist = SinglyLinkedList()
        
    def push(self, data):
        # use data as key in linked list
        self._linkedlist.insert_head(data, None)
        
    def pop(self):
        head = self._linkedlist.head()
        if head is None: return None
        self._linkedlist.remove(head)
        return head[0]
        
    def __str__(self):
        str = "Stack(["
        str += "{0}".format(list(self._linkedlist.keys()))
        return str + "])"
        

s = Stack()
s.pop()
for n in xrange(5):
    s.push(n)
    print s
for n in xrange(5):
    print s.pop()
s.pop()
print s










class _LinkedListNode:
    __slots__ = ['prev', 'data', 'next']

    def __init__(self, prev=None, data=None, next=None): 
        self.prev = prev
        self.data = data
        self.next = next






class DoublyLinkedList:

    def __init__(self, lst=None):
        # set-up special 'sentinal' node
        sentinal = _LinkedListNode(None, None, None)
        sentinal.prev = sentinal
        sentinal.next = sentinal
        self.sentinal = sentinal
        # add any items given (mostly to comply with 'construct-as-printed' pattern)
        if lst is not None: self.extend(lst)

    def insert_head(self, node):
        sentinal = self.sentinal
        next_node = sentinal.next
        next_node.prev = node
        node.next = next_node
        node.prev = sentinal
        sentinal.next = node

    def insert_tail(self, node):
        sentinal = self.sentinal
        prev_node = sentinal.prev
        prev_node.next = node
        node.prev = prev_node
        node.next = sentinal
        sentinal.prev = node

    def remove(self, node):
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node

    def head(self):
        sentinal = self.sentinal
        node = self.sentinal.next
        return node if node is not sentinal else None

    def tail(self):
        sentinal = self.sentinal
        node = self.sentinal.prev
        return node if node is not sentinal else None

    def append_head(self, data):
        node = _LinkedListNode(None, data, None)
        self.insert_head(node)
        return node

    def append_tail(self, data):
        node = _LinkedListNode(None, data, None)
        self.insert_tail(node)
        return node

    def extend(self, lst):
        for el in lst:
            self.append_tail(el)

    def search(self, data):
        sentinal = self.sentinal
        node = sentinal.next   # head
        while node is not sentinal:
            if node.data == data: return node
            node = node.next
        return None

    def __str__(self):
        str = "DoublyLinkedList(["
        sentinal = self.sentinal
        node = sentinal.next
        if node is not sentinal:
            str += "{0}".format(node.data)
            node = node.next
        while node is not sentinal:
            str += ", {0}".format(node.data)
            node = node.next
        return str + "])"

    def printlink(self):
        sentinal = self.sentinal
        node = sentinal.next
        while node is not sentinal:
            print "{0} <- {1} -> {2} ".format(node.prev.data, node.data, node.next.data)
            node = node.next
            
            
            


#
# note: 
#  - we could use a SinglyLinkedList as well if only it also kept an explicit pointer to the tail node 
#    (pushing at tail, popping at head)
#
class Queue:

    def __init__(self, lst=[]):
        self._linkedlist = DoublyLinkedList()

    def push(self, data):
        self._linkedlist.append_tail(data)

    def pop(self):
        head = self._linkedlist.head()
        if head is None: return None
        self._linkedlist.remove(head)
        return head.data