
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

    def insert_head(self, key, data):
        # form new node and make it point to old head
        node = [key, data, self.sentinal[2]]
        # make node head
        self.sentinal[2] = node

    # note: expensive because of traversal
    def insert_tail(self, key, data):
        # form new node and make it point back to sentinal
        node = [key, data, self.sentinal]
        # find tail node by traversal (ie node with next currently pointing to sentinal)
        tail_node = self.sentinal
        while tail_node[2] is not self.sentinal:
            tail_node = tail_node[2]
        # make tail node point to new node
        tail_node[2] = node

    def remove_head(self):
        # make sentinal point to the node after the current head
        node = self.sentinal[2]
        self.sentinal[2] = node[2]

    def remove_first(self, key):
        # traverse chain to find 'prev_node' pointing to 'node'
        prev_node = self.sentinal
        while prev_node[2] is not self.sentinal:
            node = prev_node[2]
            if node[0] is key:
                # make prev_node before node in the chain point to the node after node
                prev_node[2] = node[2]
                return
            else:
                # move to next
                prev_node = prev_node[2]

    def head(self):
        node = self.sentinal[2]
        return (node[0], node[1]) if node is not self.sentinal else None

    def find_first(self, key):
        # traverse chain looking for key
        node = self.sentinal[2]
        while node is not self.sentinal:
            if node[0] is key: return node[1]
            node = node[2]
        return None
        
    def keys(self):
        # traverse entire chain
        node = self.sentinal[2]
        while node is not self.sentinal:
            yield node[0]
            node = node[2]
            
    def items(self):
        # traverse entire chain
        node = self.sentinal[2]
        while node is not self.sentinal:
            yield (node[0], node[1])
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


#sl = SinglyLinkedList()
#for n in xrange(5,0,-1):
#    sl.insert_head(n, n*10)
#    print sl
#for m in xrange(6,11):
#    sl.insert_tail(m, m*10)
#    print sl
#for l in xrange(10+1):
#    sl.remove_head()
#    print sl






class Stack:

    def __init__(self, lst=[]):
        self._linkedlist = SinglyLinkedList(map(lambda el: (el, None), lst))
        
    def push(self, data):
        # use data as key in linked list
        self._linkedlist.insert_head(key=data, data=None)
        
    def pop(self):
        head = self._linkedlist.head()
        self._linkedlist.remove_head()
        return head[0] if head is not None else None
        
    def __str__(self):
        str = "Stack("
        keys = self._linkedlist.keys()
        str += "{0}".format(list(keys))
        return str + ")"
        

#s = Stack()
#s.pop()
#for n in xrange(5):
#    s.push(n)
#    print s
#for n in xrange(5):
#    print s.pop()
#s.pop()
#print s










class LinkedListNode:
    __slots__ = ['key', 'data', 'prev', 'next']

    def __init__(self, key, data=None, prev=None, next=None):
        self.key = key
        self.data = data
        self.prev = prev
        self.next = next


# note that this linked list (unlike the singly linked list) exposes the nodes instead of hiding behind keys
class DoublyLinkedList:

    def __init__(self, lst=None):
        # set-up special 'sentinal' node
        sentinal = LinkedListNode(None, None, None, None)
        sentinal.prev = sentinal
        sentinal.next = sentinal
        self.sentinal = sentinal
        # add any items given (mostly to comply with 'construct-as-printed' pattern)
        if lst is not None: self.extend(lst)

    def insert(self, prev_node, node, next_node):
        # insert at location
        node.prev = prev_node
        node.next = next_node
        prev_node.next = node
        next_node.prev = node

    def insert_head(self, node):
        # find location
        prev_node = self.sentinal
        next_node = self.sentinal.next
        # insert at location
        self.insert(prev_node, node, next_node)
        
    def insert_tail(self, node):
        # find location
        prev_node = self.sentinal.prev
        next_node = self.sentinal
        # insert at location
        self.insert(prev_node, node, next_node)

    def remove(self, node):
        # find surrounding nodes
        prev_node = node.prev
        next_node = node.next
        # remove node from chain
        prev_node.next = next_node
        next_node.prev = prev_node

    def remove_head(self):
        head = self.sentinal.next
        self.remove(head)
        
    def remove_tail(self):
        tail = self.sentinal.prev
        self.remove(tail)

    def head(self):
        head = self.sentinal.next
        return head if head is not self.sentinal else None

    def tail(self):
        tail = self.sentinal.prev
        return tail if tail is not self.sentinal else None

    def extend(self, lst):
        for pair in lst:
            node = LinkedListNode(pair[0], pair[1])
            self.insert_tail(node)

    def nodes(self):
        node = self.sentinal.next
        while node is not self.sentinal:
            yield node
            node = node.next

    def __str__(self):
        str = "DoublyLinkedList(["
        sentinal = self.sentinal
        node = sentinal.next
        if node is not sentinal:
            str += "({0}, {1})".format(node.key, node.data)
            node = node.next
        while node is not sentinal:
            str += ", ({0}, {1})".format(node.key, node.data)
            node = node.next
        return str + "])"

    def printchain(self):
        sentinal = self.sentinal
        node = sentinal.next
        while node is not sentinal:
            print "{0} <- {1} -> {2} ".format(node.prev.key, node.key, node.next.key)
            node = node.next
            
            
            

#dl = DoublyLinkedList()
#for n in xrange(5,0,-1):
#    node = LinkedListNode(n, n*10)
#    dl.insert_head(node)
#    print dl
#for m in xrange(6,11):
#    node = LinkedListNode(m, m*10)
#    dl.insert_tail(node)
#    print dl
#for l in xrange(10+1):
#    dl.remove_head()
#    print dl
            
            


#
# note: 
#  - we could use a SinglyLinkedList as well if only it also kept an explicit pointer to the tail node 
#    (pushing at tail, popping at head)
#
class Queue:

    def __init__(self, lst=[]):
        self._linkedlist = DoublyLinkedList(map(lambda el: (el, None), lst))

    def push(self, item):
        node = LinkedListNode(key=item)
        self._linkedlist.insert_tail(node)

    def pop(self):
        head = self._linkedlist.head()
        if head is None: return None
        self._linkedlist.remove(head)
        return head.key
        
    def __str__(self):
        str = "Queue("
        keys = ( node.key for node in self._linkedlist.nodes() )
        str += "{0}".format(list(keys))
        return str + ")"
        

#q = Queue()
#for n in xrange(5):
#    q.push(n)
#    print q
#for n in xrange(5):
#    print q.pop()
#q.pop()
#print q





class LruCache:
    
    # assume that max_size > 0
    def __init__(self, max_size):
        self.max_size = max_size
        self.size = 0
        self.store = dict()
        self.order = DoublyLinkedList()

    def get(self, key):
        if not key in self.store: return None  # cache miss
        (data, node) = self.store[key]
        self.order.remove(node)
        self.order.insert_head(node)
        return data

    # assume that key doesn't already exist in cache (needed for order)
    def put(self, key, data):
        if not self.size < self.max_size:
            # remove least-recently item first
            # .. from order
            tail_node = self.order.tail()
            self.order.remove(tail_node)
            # .. from store
            self.store.pop(tail_node.key, None)
            self.size -= 1
        node = LinkedListNode(key)
        self.order.insert_head(node)
        self.store[key] = (data, node)
        self.size += 1
        
        
#lc = LruCache(3)
#lc.put(1,10)
#print lc.order
#lc.put(2,20)
#print lc.order
#lc.put(3,30)
#print lc.order
#lc.get(1)
#print lc.order
#lc.put(4,40)
#print lc.order



