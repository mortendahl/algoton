



from linkedlist import DoublyLinkedList


class LRUCache:
    
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
            
    def put(self, key, data):
        if not self.size < self.max_size:
            # remove least-recently item first
            # .. from order
            tail = self.order.tail()
            old_key = tail.data
            self.order.remove(tail)
            # .. from store
            self.store.pop(old_key, None)
            self.size -= 1
        node = self.order.append_head(key)
        self.store[key] = (data, node)
        self.size += 1



