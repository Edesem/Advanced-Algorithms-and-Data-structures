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
        self.root = None
        self.count = 0
        self.max = max

    def insert(self, key):
        # Base case, first insertion
        node = Node(key)

        if self.count == 0:
            self.root = node
            self.count += 1
        elif self.root.get_length() < self.max:
            self.root.insert(key)
            self.count += 1


    def delete(self):
        pass

    def search(self):
        pass