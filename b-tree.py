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
        if self.count == 0:
            node = Node(key)
            self.root = node
            self.count += 1

        elif self.root.get_length() < self.max:
            self.root.insert(key)
            self.count += 1

        # Root layer is max capacity
        else:
            keys = self.root.keys
            keys.sort()
            n = len(keys)
            median = keys[n // 2]

            print(median)

    def delete(self):
        pass

    def search(self):
        pass

t = Tree(3)
t.insert(7)
t.insert(23)
t.insert(59)
t.insert(73)