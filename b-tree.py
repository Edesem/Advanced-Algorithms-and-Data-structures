class Node():
    def __init__(self, key):
        self.keys = [key]
        self.children = None
        self.parent = None

    def insert(self, key):
        self.keys.append(key)

    def get_length(self):
        return len(self.keys)
    
class Tree():
    def __init__(self, max):
        self.count = 0
        self.max = max

    def insert(self, key):
        # Base case, first insertion
        if self.count == 0:
            node = Node(key)
            self.count += 1

    def delete(self):
        pass

    def search(self):
        pass