class Node():
    def __init__(self, key):
        self.key = key
        self.degree = 0
        self.mark = False

        self.parent = None 
        self.child = None
        self.left = None
        self.right = None

class FibonacciHeap():
    def __init__(self):
        self.count = 0
        self.min = None
        self.root_list = None

    def insert(self, key):
        node = Node(key) 
        node.left = node
        node.right = node

        self.join_root_list(node)

        if key < self.min.key:
            self.min = node
        
        self.count += 1
        return node

    def join_root_list(self, node):
        if self.root_list is None:
            self.root_list = node
        else:
            node.right = self.root_list
            node.left = self.root_list.left
            self.root_list.left.right = node
            self.root_list.left = node

    def min(self):
        return self.min
    
    def extract_min(self):
        min_node = self.min()
        if min_node.children is None:
            min_node.left.right = min_node.right
            min_node.right.left = min_node.left
            self.consolidate()



        return min.key

    def consolidate(self):
        min = self.min()
        current_node = min
        next_node = current_node.right

        while current_node != min:
            while next_node != min: 
                if current_node.degree != next_node.degree:
                    next_node = next_node.right
                    continue
                else:
                    if current_node.key < next_node.key:
                        if current_node.children == None:
                            current_node.children = next_node
                            next_node.parent = current_node
                            next_node.left = next_node
                            next_node.right = next_node
                        else:
                            next_node.parent = current_node
                            next_node.left = current_node.children.left
                            next_node.right = current_node.children.right
                            current_node.left.right = next_node
                            current_node.right = next_node
    def merge(self):
        pass

    def decrease_key(self):
        pass

    def delete(self):
        pass