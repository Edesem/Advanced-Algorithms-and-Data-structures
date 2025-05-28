from string import ascii_uppercase

class Node():
    def __init__(self, key=None):
        if key is None:
            self.keys = []
        else:
            self.keys = [key]
        self.children = []
        self.parent = None

    def insert(self, key):
        # Binary search to find insertion index
        low, high = 0, len(self.keys)
        while low < high:
            mid = (low + high) // 2
            if self.keys[mid] < key:
                low = mid + 1
            else:
                high = mid
        self.keys.insert(low, key)

    def get_length(self):
        return len(self.keys)
    
    def is_leaf(self):
        return len(self.children) == 0
    
    def delete(self, index):
        return self.keys.pop(index)
    
class Tree():
    def __init__(self, t):
        self.root = None
        self.count = 0
        self.max = (t * 2) - 1
        self.min = t - 1
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
            return
    
        node = self._node_to_insert(key, self.root)

        if node.get_length() >= self.max:
            self.split(node)

            node = self._node_to_insert(key, self.root)

        node.insert(key)
        self.count += 1

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
        if parent and len(parent.keys) >= self.max:
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

    def delete(self, key, node=None):
        # When called for the first time
        if node is None:
            node = self.root

        if key in node.keys:
            index = node.keys.index(key)
            if node.is_leaf():
                # Case 1
                if node.get_length() > self.min:
                    node.delete(index)
                # Case 3a
                else:
                    print(f"Deleting {node.keys}")
                    parent = node.parent
                    i = 0
                    while i < len(parent.children) and parent.children[i] != node:
                        i += 1

                    self.fix_child_if_needed(parent, i)

                    # Re-access node via index (not reference)
                    node = parent.children[i]
                    if key in node.keys:
                        node.delete(node.keys.index(key))

                
            # Case 2
            else:
                index = node.keys.index(key)

                left_child = node.children[index] 
                right_child = node.children[index + 1]

                # Case 2a, borrow from the predecessor
                if len(left_child.keys) >= self.min + 1:
                    predecessor = self.get_predecessor(left_child)
                    node.keys[index] = predecessor
                    self.delete(predecessor, left_child)
                # Case 2b, borrow from sucessor
                elif len(right_child.keys) >= self.min + 1:
                    successor = self.get_successor(right_child)
                    node.keys[index] = successor
                    self.delete(successor, right_child)
                # Case 2c, merging
                else:
                    self.merge(left_child, right_child, node, index)
                    self.delete(key, left_child)

        # When key not in node
        else:
            # Step 1: find child index
            i = 0
            while i < len(node.keys) and key >= node.keys[i]:
                i += 1

            # Step 2: fix underflow before descending
            i = self.fix_child_if_needed(node, i)

            # Step 4: descend safely
            return self.delete(key, node.children[i])
            
    def fix_child_if_needed(self, parent, i):
        child = parent.children[i]
        if child.get_length() == self.min:
            left_sibling = parent.children[i - 1] if i > 0 else None
            right_sibling = parent.children[i + 1] if i + 1 < len(parent.children) else None

            # Case 3a: borrow from left
            if left_sibling and left_sibling.get_length() > self.min:
                borrowed_key = left_sibling.keys.pop(-1)
                parent_key = parent.keys[i - 1]
                parent.keys[i - 1] = borrowed_key
                child.keys.insert(0, parent_key)
                return i

            # Case 3a: borrow from right
            elif right_sibling and right_sibling.get_length() > self.min:
                borrowed_key = right_sibling.keys.pop(0)
                parent_key = parent.keys[i]
                parent.keys[i] = borrowed_key
                child.keys.append(parent_key)
                return i

            # Case 3b: merge
            elif left_sibling:
                self.merge(left_sibling, child, parent, i - 1)
                return i - 1
            elif right_sibling:
                self.merge(child, right_sibling, parent, i)
                return i
            
        return i

    def get_predecessor(self, node):
        while not node.is_leaf():
            node = node.children[-1]
        return node.keys[-1]
    
    def get_successor(self, node):
        while not node.is_leaf():
            node = node.children[0]
        return node.keys[0]

    def merge(self, left_child, right_child, node, index):
        # Pull down key to left child
        seperator_key = node.delete(index)
        left_child.keys.append(seperator_key)

        # add right child keys to left child
        left_child.keys.extend(right_child.keys)

        if not right_child.is_leaf():
            left_child.children.extend(right_child.children)
            
        # Remove seperator key and right child
        node.children.pop(index + 1)

        # Prevents root being empty after a merge
        if self.root.get_length() == 0 and not self.root.is_leaf():
            self.root = self.root.children[0]
            self.root.parent = None


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

    

"""node.delete(index)
t = Tree(4)
t.insert(7)
t.insert(23)
t.insert(59)
t.insert(73)
t.insert(93)
t.insert(25)

t = Tree(2)
t.search(1)

t = Tree(2)
t.insert(1)
t.insert(2)
t.insert(3)
t.search(2)


t = Tree(2)
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
t.insert(16)


t.delete(7)

t.print_tree()


t = Tree(2)
for key in ascii_uppercase:  # 'A' to 'Z'
    t.insert(key)
    print(f"INSERTING {key}")
    t.print_tree()


print("\n\n\nCOMPLETE TREE")
t.print_tree()

for key in ["C", "I", "H", "G", "B", "A"]:
    print(f"\nDeleting {key}")
    t.delete(key)
    t.print_tree()

"""

t = Tree(3)
for key in [47, 13, 82, 59, 6, 91, 34, 28, 75, 99, 4, 66, 51, 88, 22, 39, 15, 93, 11, 70, 61, 62, 63, 64]: 
    t.insert(key)
    print(f"INSERTING {key}")
    t.print_tree()


print("\n\n\nCOMPLETE TREE")
t.print_tree()

for key in ["C", "I", "H", "G", "B", "A"]:
    print(f"\nDeleting {key}")
    t.delete(key)
    t.print_tree()