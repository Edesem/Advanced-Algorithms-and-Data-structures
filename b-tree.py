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
    
class Tree():
    def __init__(self, max):
        self.root = None
        self.count = 0
        self.max = max

    def insert(self, key, node=None):
        # Base case, first insertion
        if self.root is None:
            node = Node(key)
            self.root = node
            self.count += 1

        elif self.root.get_length() < self.max:
            result = self._insert_helper_(key, self.root)
            if self.root.children is not None:
                pass
            else:
                self.root.insert(key)
                self.count += 1

        # Root layer is max capacity
        else:
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

    def _insert_helper_(self, key, root):
        if root.children is not None:
            for i in range(root.get_length()):
                if key < self.root.keys[i]:
                    self.children[i].insert(key)
                if key > self.root.keys[i]:
                    self.children[i + 1].insert(key)

    def delete(self):
        pass

    def search(self):
        pass

t = Tree(4)
t.insert(7)
t.insert(23)
t.insert(59)
t.insert(73)
t.insert(93)
t.insert(25)