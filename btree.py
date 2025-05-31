import random

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
        self.count = 0 # Debugging purposes
        self.max = (t * 2) - 1
        self.min = t - 1
        self.t = t
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
            self._split(node)

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
    def _split(self, node):
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
            index = parent.children.index(node)
            parent.children.pop(index)
            parent.children.insert(index, left)
            parent.children.insert(index + 1, right)
            left.parent = right.parent = parent
            parent.insert(median)

        # If parent now overflows, split it too
        if parent and len(parent.keys) >= self.max:
            self._split(parent)

    def search(self, key):
        if key not in self.set:
            print(f"Key {key} not found in tree.")
            return None

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
                node = node.children[-1]

        index = node.keys.index(key)
        print(f"Found key ({key}) in {node.keys} at {index}")
        return node, index

    def delete(self, key, node=None):
        if key not in self.set:
            print(f"Key {key} not found in tree.")
            return 
        
        # When called for the first time
        if node is None:
            node = self.root

        if key in node.keys:
            index = node.keys.index(key)
            if node.is_leaf():
                # Case 1
                if node.get_length() > self.min:
                    node.delete(index)
                    self.set.discard(key)
                    self.count -= 1
                
            # Case 2
            else:
                index = node.keys.index(key)

                left_child = node.children[index] 
                right_child = node.children[index + 1]

                # Case 2a, borrow from the predecessor
                if len(left_child.keys) >= self.t:
                    predecessor = self._get_predecessor(left_child)
                    node.keys[index] = predecessor
                    self.delete(predecessor, left_child)
                # Case 2b, borrow from sucessor
                elif len(right_child.keys) >= self.t:
                    successor = self._get_successor(right_child)
                    node.keys[index] = successor
                    self.delete(successor, right_child)
                # Case 2c, merging
                else:
                    self._merge(left_child, right_child, node, index)
                    self.delete(key, left_child)

        # When key not in node
        else:
            # Find child index
            i = 0
            while i < len(node.keys) and key >= node.keys[i]:
                i += 1

            # Fix underflow before descending
            i = self._fix_child_if_needed(node, i)

            # Descend safely
            return self.delete(key, node.children[i])
            
    def _fix_child_if_needed(self, parent, i):
        child = parent.children[i]
        if child.get_length() <= self.min:
            print(child.keys)
            left_sibling = parent.children[i - 1] if i > 0 else None
            right_sibling = parent.children[i + 1] if i + 1 < len(parent.children) else None

            # Case 3b: Merge
            if left_sibling and left_sibling.get_length() == self.min:
                self._merge(left_sibling, child, parent, i - 1)
                return i - 1
            elif right_sibling and right_sibling.get_length() == self.min:
                self._merge(child, right_sibling, parent, i)
                return i

            # Case 3a: borrow from left
            elif left_sibling and left_sibling.get_length() > self.min:
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

        return i

    def _get_predecessor(self, node):
        while not node.is_leaf():
            node = node.children[-1]
        return node.keys[-1]
    
    def _get_successor(self, node):
        while not node.is_leaf():
            node = node.children[0]
        return node.keys[0]

    def _merge(self, left_child, right_child, node, index):
        # Pull down key to left child
        seperator_key = node.delete(index)
        left_child.keys.append(seperator_key)

        # add right child keys to left child
        left_child.keys.extend(right_child.keys)

        # Add all the children of the right node to the left node
        if not right_child.is_leaf():
            left_child.children.extend(right_child.children)
            
        # Remove right child
        node.children.pop(node.children.index(right_child))
        
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

    def select(self, k, node=None, counter=None):        
        # Uses in order tree traversal as basis

        if counter == None:
            # So it is mutable and persists during recursion
            counter = [1]
        
        if node == None:
            node = self.root

        if not node.is_leaf():
            for i, key in enumerate(node.keys):
                # Go left
                res = self.select(k, node.children[i], counter)
                if res != -1:
                    return res

                # Visit
                if counter[0] == k:
                    return key
                
                counter[0] += 1

            # Traverse right-most branch
            res = self.select(k, node.children[len(node.keys)], counter)
            if res != -1:
                return res

        else:
            for key in node.keys:
                # Visit
                if counter[0] == k:
                    return key
                counter[0] += 1

        return -1

    def rank(self, x, node=None, rank=None):
        # Uses in order tree traversal as basis

        # If key not in tree
        if x not in self.set: 
            return -1
        
        if rank == None:
            # So it is mutable and persists during recursion
            rank = [0]
        
        if node == None:
            node = self.root

        if not node.is_leaf():
            for i, key in enumerate(node.keys):
                # Go left
                self.rank(x, node.children[i], rank)

                # Visit
                if key < x:
                    rank[0] += 1
                elif key == x:
                    rank[0] += 1
                    return rank[0]

            # Traverse right-most branch
            self.rank(x, node.children[len(node.keys)], rank)

        else:
            for key in node.keys:
                # Visit
                if key < x:
                    rank[0] += 1
                elif key == x:
                    rank[0] += 1
                    return rank[0]

        return rank[0]

    def keysInRange(self, x, y, node=None, keys=None):
        # Uses in order tree traversal as basis

        if keys == None:
            keys = []
 
        if node == None:
            node = self.root

        if not node.is_leaf():
            for i, key in enumerate(node.keys):
                # Traverse left
                if x < key:
                    self.keysInRange(x, y, node.children[i], keys)
                    
                # Visit
                if x <= key <= y:
                    keys.append(key)

            # Traverse right-most branch
            self.keysInRange(x, y, node.children[len(node.keys)], keys)

        else:
            for key in node.keys:
                if x <= key <= y:
                    keys.append(key)

        # None found
        if len(keys) == 0:
            return -1
        return keys

    def primesInRange(self, x, y, node=None, keys=None):
        # Uses in order tree traversal as basis

        if keys == None:
            keys = []
 
        if node == None:
            node = self.root

        if not node.is_leaf():
            for i, key in enumerate(node.keys):
                # Traverse left
                if x < key:
                    self.primesInRange(x, y, node.children[i], keys)
                    
                # Visit
                if x <= key <= y and self._is_prime(key):
                    keys.append(key)

            # Traverse right-most branch
            self.primesInRange(x, y, node.children[len(node.keys)], keys)

        else:
            for key in node.keys:
                if x <= key <= y and self._is_prime(key):
                    keys.append(key)

        # None found
        if len(keys) == 0:
            return -1
        return keys
    
    def _is_prime(self, n):
        # Miller-Rabin-Randomised-Primality-Checker

        # Number of iterations (Hard coded for simplicity)
        k = 20

        # Special case
        if n == 2 or n == 3:
            return True
        
        # If n is even
        if n < 2 or n % 2 == 0:
            return False
        
        # Factor n - 1 as (2^s)*t, where t is odd
        s = 0
        t = n - 1
        while t % 2 == 0:
            s = s + 1
            t = t // 2
        
        # Run k random tests
        for _ in range(k):
            # Select random witness
            a = random.randrange(1,n-1)
            x = pow(a, t, n)  # x0 = a^t mod n


            # Check if n satisfies fermat's little theorem for this witness
            if x == 1 or x == n - 1:
                continue
            
            # Run sequence test
            for _ in range(s):
                x = pow(x, 2, n)

                if x == n - 1:
                    break
                if x == 1:
                    # x_j == 1 and x_{j-1} != 1 and != n-1
                    return False
            else:
                return False  # Composite
        
        # If n has passed all tests, then it's probably a prime
        return True

def main():    
    t = Tree(3)
    for key in [47, 13, 82, 59, 6, 91, 34, 28, 75, 99, 4, 66, 51, 88, 22, 39, 15, 93, 11, 70, 61, 62, 63, 64, 40]: 
        t.insert(key)
        print(f"INSERTING {key}")
        t.print_tree()


    print("\n\n\nCOMPLETE TREE")
    t.print_tree()

    for key in [47, 75, 70, 66, 1]:
        print(f"\nDeleting {key}")
        t.delete(key)
        t.print_tree()