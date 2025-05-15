class Node():
    def __init__(self, key=None):
        if key is None:
            self.keys = []
        else:
            self.keys = [key]
        self.children = None
        self.parent = None

    def insert(self, key):
        self.keys.append(key)

    def get_length(self):
        return len(self.keys)
    
    def is_leaf(self):
        return self.get_length() == 0
    
class Tree():
    def __init__(self, max):
        self.root = None
        self.count = 0
        self.max = max

    def insert(self, key, node=None):
        # Base case, first insertion
        if self.root is None:
            self.root = Node(key)
            self.count += 1
            return
        

        elif self.root.get_length() < self.max:
            result = self._insert_helper_(key, self.root)
            if self.root.children is not None:
                pass
            else:
                self.root.insert(key)
                self.count += 1

        # Root layer is max capacity
        else:
            self.split(key)


    def _node_to_insert(self, key, node):
        while not node.is_leaf():
            for i, value in enumerate(node.keys):
                if key < value:
                    node = node.children[i]
                    break
            else:
                node = node.children[-1]

        return node
    
    def split(self, key):
        self.root.insert(key)
        keys = self.root.keys
        keys.sort()
        print(keys)
        median_index = len(keys) // 2
        median = keys[median_index]

        # Left node
        left = Node()
        for i in range(median_index):
            left.insert(keys[i])
            print(keys[i])

        right = Node()
        for i in range(median_index + 1, len(keys)):
            right.insert(keys[i])
            print(keys[i])

        new_root = Node(median)
        new_root.children = [left, right]
        left.parent = new_root
        right.parent = new_root
        
        self.root = new_root

        print(left.keys, right.keys, new_root.keys)

    def delete(self):
        pass

    def search(self):
        pass

"""
t = Tree(4)
t.insert(7)
t.insert(23)
t.insert(59)
t.insert(73)
t.insert(93)
t.insert(25)
"""

t = Tree(2)
t.insert(1)
t.insert(2) 
t.insert(3)