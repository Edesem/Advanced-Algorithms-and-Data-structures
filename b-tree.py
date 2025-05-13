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

    def insert(self, key):
        # Base case, first insertion
        if self.count == 0:
            node = Node(key)
            self.root = node
            self.count += 1

        elif self.root.get_length() < self.max:
            if self.root.children is not None:
                pass
            else:
                self.root.insert(key)
                self.count += 1

        # Root layer is max capacity
        else:
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

t = Tree(7)
t.insert(7)
t.insert(23)
t.insert(59)
t.insert(73)
t.insert(2)
t.insert(21)
t.insert(1)
t.insert(11)