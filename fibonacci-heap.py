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

    def minimum(self):
        return self.min