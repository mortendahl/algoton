
from linkedlist import SinglyLinkedList

# for universal hashing
import random

class Hashtable:

    # assume that size < 137
    def __init__(self, size, items=[]):
        self._size = size
        # initialise
        self._table = [None]*size
        #
        # ***** select hash function *****
        #
        # - division hash function:
        #
        #self._hash_function = lambda key: key % size
        #
        # - universal hash function:
        #
        prime = 137  # we must have size < prime, see Cormen et al. page 234-235
        a = random.choice(xrange(1,prime))
        b = random.choice(xrange(0,prime))
        self._hash_function = lambda key: ((a*key + b) % prime) % size
        #
        # ***** END select hash function *****
        #
        # finally, insert any items
        for (key,data) in items: self.insert(key,data)

    # assume that key isn't already in the table; must be manually removed first if it is
    def insert(self, key, data):
        hash = self._hash_function(key)
        if self._table[hash] is None: self._table[hash] = SinglyLinkedList() 
        self._table[hash].insert_head(key, data)

    def search(self, key):
        hash = self._hash_function(key)
        if self._table[hash] is None: return None
        return self._table[hash].find_first(key)

    def delete(self, key):
        hash = self._hash_function(key)
        if self._table[hash] is not None:
            self._table[hash].remove_first(key)

    def items(self):
        return (item for lst in self._table if lst is not None for item in lst.items())


#h = Hashtable(10)
#h.insert(1,10)
#h.insert(2,20)
#print list(h.items())