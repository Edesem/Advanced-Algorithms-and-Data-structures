class Node():
    def __init__(self, key=None):
        if key is None:
            self.keys = []
        else:
            self.keys = [key]
        self.children = []
        self.parent = None

    def insert(self, key):
        self.keys.append(key)

    def get_length(self):
        return len(self.keys)
    
    def is_leaf(self):
        return len(self.children) == 0
    
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
            print(f"Inserted key {key}")
            self.print_tree()
            print()
            return
    
        node = self._node_to_insert(key, self.root)
        
        if node.get_length() == self.max:
            self.split(key, node)
        else:
            node.insert(key)

        print(f"Inserted key {key}")
        self.print_tree()
        print()


    def _node_to_insert(self, key, node):
        while not node.is_leaf():
            for i, value in enumerate(node.keys):
                if key < value:
                    node = node.children[i]
                    break
            else:
                node = node.children[-1]

        return node
    
    def split(self, key, node):
        node.insert(key)
        keys = node.keys
        keys.sort()

        median_index = len(keys) // 2
        median = keys[median_index]

        # Left node
        left = Node()
        for i in range(median_index):
            left.insert(keys[i])

        right = Node()
        for i in range(median_index + 1, len(keys)):
            right.insert(keys[i])

        new_parent = Node(median)
        new_parent.children = [left, right]
        left.parent = new_parent
        right.parent = new_parent
        
        self.root = new_parent

    def delete(self):
        pass

    def search(self):
        pass

    def print_tree(self, node=None, indent="", is_last=True):
        if node is None:
            node = self.root
        if node is None:
            print("Empty tree.")
            return

        prefix = indent + ("└── " if is_last else "├── ")
        print(prefix + str(node.keys))

        if node.children:
            for i, child in enumerate(node.children):
                is_last_child = (i == len(node.children) - 1)
                self.print_tree(child, indent + ("    " if is_last else "│   "), is_last_child)

    

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
t.insert(4)
t.insert(5)