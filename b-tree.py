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
    
    def delete(self, index):
        self.keys.pop(index)
    
class Tree():
    def __init__(self, max):
        self.root = None
        self.count = 0
        self.max = max
        self.set = set()
        
    def insert(self, key, node=None):
        if key not in self.set:
            self.set.add(key) 
        else:
            print(f"Key ({key}) already exists, duplicates not allowed")
            return

        # Base case, first insertion
        if self.root is None:
            self.root = Node(key)
            self.count += 1
            print(f"Inserted key {key}")
            self.print_tree()
            print()
            return
    
        node = self._node_to_insert(key, self.root)

        node.insert(key)
        self.count += 1
        if node.get_length() >= self.max:
            self.split(node)

        #print(f"Inserted key {key}")
        #self.print_tree()
        #print()

    # Find node to insert into
    def _node_to_insert(self, key, node):
        while not node.is_leaf():
            for i, value in enumerate(node.keys):
                if key < value:
                    node = node.children[i]
                    break
            else:
                node = node.children[-1]

        return node
    
    # Split specified node up
    def split(self, node):
        keys = node.keys
        keys.sort()

        median_index = len(keys) // 2
        median = keys[median_index]

        # Left node
        left = Node()
        right = Node()
        left.keys = keys[:median_index]
        right.keys = keys[median_index+1:]

            
        # Carry over children if internal node
        if node.children:
            left.children = node.children[:median_index + 1]
            right.children = node.children[median_index + 1:]
            for child in left.children:
                child.parent = left
            for child in right.children:
                child.parent = right

        parent = node.parent
        # case 1: node was root
        if parent is None:
            new_root = Node(median)
            new_root.children = [left, right]
            left.parent = right.parent = new_root
            self.root = new_root

        # case 2: promote median to parent
        else:
            idx = parent.children.index(node)
            parent.children.pop(idx)
            parent.children.insert(idx, left)
            parent.children.insert(idx + 1, right)
            left.parent = right.parent = parent
            parent.insert(median)


        # If parent now overflows, split it too
        if parent and len(parent.keys) > self.max:
            self.split(parent)

    def search(self, key):
        if self.root is None:
            print(f"Key ({key}) does not exist - empty tree")
            return None
        
        node = self.root
        while key not in node.keys:
            for i, value in enumerate(node.keys):
                if key < value:
                    node = node.children[i]
                    break
            else:
                if len(node.children) == 0:
                    print(f"Key ({key}) does not exist")
                    return None
                
                node = node.children[-1]

        index = node.keys.index(key)
        print(f"Found key ({key}) in {node.keys} at {index}")
        return node, index

    def delete(self, key):
        node, index = self.search(key)
        node.delete(index)
        min = self.max // 2

        if len(node.keys) < min:
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
t.search(1)

t = Tree(2)
t.insert(1)
t.insert(2)
t.insert(3)
t.search(2)


t = Tree(4)
t.insert(1)
t.insert(2) 
t.insert(3)
t.insert(4)
t.insert(5)
t.insert(6)
t.insert(7)
t.insert(8)
t.insert(9)
t.insert(10)
t.insert(11)
t.insert(12)
t.insert(13)
t.insert(14)
t.insert(15)
t.insert(15)

print(t.count)

t.search(15)

t.delete(14)