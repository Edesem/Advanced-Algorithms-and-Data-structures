class Node():
    def __init__(self, key):
        self.key = key
        self.degree = 0
        self.mark = False

        self.parent = None 
        self.child = None
        self.left = None
        self.right = None

    def __str__(self) -> str:
        return f"Node(key={self.key}, degree={self.degree}, parent={self.parent.key if self.parent else None}, child={self.child.key if self.child else None})"


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

        if self.min is None or key < self.min.key:
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
    
    def extract_min(self):
        min_node = self.minimum()
        if min_node.children is None:
            min_node.left.right = min_node.right
            min_node.right.left = min_node.left
            self.consolidate()

        return min.key

    def consolidate(self):
        min = self.minimum()
        current_node = min
        next_node = current_node.right

        # Do While loop
        while True:
            while next_node != min: 
                if current_node.degree != next_node.degree:
                    next_node = next_node.right
                    continue
                else:
                    # Determine new parent and child
                    if current_node.key < next_node.key:
                        child, parent = next_node, current_node
                    else:
                        child, parent = current_node, next_node

                    if parent.children == None:
                        parent.children = child
                        child.parent = parent
                        child.left = child
                        child.right = child
                    else:
                        child.parent = parent
                        child.left = parent.children.left
                        child.right = parent.children.right
                        parent.left.right = child
                        parent.right = child
                
                next_node = next_node.right

            current_node = current_node.right
            next_node = current_node.right
            if current_node == min:
                break
                        
    def merge(self):
        pass

    def decrease_key(self):
        pass

    def delete(self):
        pass

    def __str__(self):
        if self.root_list is None:
            return "FibonacciHeap(empty)"

        result = ["FibonacciHeap:"]
        node = self.root_list
        visited = set()

        def visit(node):
            return f"(key={node.key}, degree={node.degree})"

        result.append("Root List:")
        current = node
        while True:
            result.append("  " + visit(current))
            visited.add(current)
            current = current.right
            if current == node or current in visited:
                break

        result.append(f"Min: {self.min.key if self.min else 'None'}")
        result.append(f"Total Nodes: {self.count}")
        return "\n".join(result)

fh = FibonacciHeap()
fh.insert(3)
fh.insert(5)
fh.insert(7)
fh.insert(9)
fh.extract_min()
print(fh)