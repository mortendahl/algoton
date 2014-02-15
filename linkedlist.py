
#
# Functional alternative at http://stackoverflow.com/questions/280243/python-linked-list#280284
#




#
#  Singly linked-list using Python lists as nodes: [data, next]
#
#
#  notes:
#   - uses special 'sentinal' node to indicate 'end of list'; sentinal[1] is head of list
#

class SinglyLinkedList:

    def __init__(self, lst=[]):
        # set-up special 'sentinal' node
        sentinal = [None, None]   # [data, next]
        sentinal[1] = sentinal
        self.sentinal = sentinal
        # add any items given (to comply with 'construct-as-printed' pattern)
        self.extend(lst)

    def insert_head(self, node):
        node[1] = self.sentinal[1]
        self.sentinal[1] = node

    def insert_tail(self, node):
        # traverse list to find tail; tail is the node with next pointing to sentinal
        tail_node = self.sentinal
        while tail_node[1] is not self.sentinal:
            tail_node = tail_node[1]
        # append at tail
        tail_node[1] = node
        node[1] = self.sentinal

    # assume that 'node' is not sentinal
    def remove(self, node):
        # traverse list to find 'prev_node' pointing to 'node'
        prev_node = self.sentinal
        while prev_node[1] is not self.sentinal:
            if prev_node[1] is node:
                # remove and return
                prev_node[1] = node[1]
                return
            else:
                # move to next
                prev_node = prev_node[1]

    def head(self):
        node = self.sentinal[1]
        # check if empty list
        return node if node is not self.sentinal else None

    def tail(self):
        # traverse list to find tail
        tail_node = self.sentinal
        while tail_node[1] is not self.sentinal:
            tail_node = tail_node[1]
        # check if empty list
        return tail_node if tail_node is not self.sentinal else None

    def append_head(self, data):
        self.sentinal[1] = [data, self.sentinal[1]]

    def append_tail(self, data):
        node = [data, None]
        self.insert_tail(node)
        return node

    def extend(self, lst):
        for el in reversed(lst):
            self.append_head(el)

    def search(self, data):
        # traverse list
        node = self.sentinal[1]
        while node is not self.sentinal:
            if node[0] == data: return node
            node = node[1]
        return None

    def __str__(self):
        str = "SinglyLinkedList(["
        node = self.sentinal[1]
        if node is not self.sentinal:
            str += "{0}".format(node[0])
            node = node[1]
        while node is not self.sentinal:
            str += ", {0}".format(node[0])
            node = node[1]
        return str + "])"

    def printlink(self):
        node = self.sentinal[1]
        while node is not self.sentinal:
            print "{0} {1} ".format(node[0], "->" if node[1] is not self.sentinal else "  ")
            node = node[1]


#s = SinglyLinkedList()
#for n in xrange(5,0,-1):
#    s.append_head(n)
#    print s
#for m in xrange(6,11):
#    s.append_tail(m)
#    print s






class Stack:

    def __init__(self, lst=[]):
        self._linkedlist = SinglyLinkedList()
        
    def push(self, data):
        self._linkedlist.append_head(data)
        
    def pop(self):
        head = self._linkedlist.head()
        if head is None: return None
        self._linkedlist.remove(head)
        return head[0]
        













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