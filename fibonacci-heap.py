import math

class Node():
    def __init__(self, key):
        self.key = key
        self.degree = 0
        self.mark = False

        self.parent = None 
        self.children = None
        self.left = None
        self.right = None

    def __str__(self) -> str:
        return f"Node(key={self.key}, degree={self.degree}, parent={self.parent.key if self.parent else None}, child={self.children.key if self.children else None})"


class FibonacciHeap():
    def __init__(self):
        self.count = 0
        self.min = None
        self.root_list = None

    def insert(self, key):
        self.print_root_list()
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

        print(f"Post insertion for {node.key}\n", node.left, '\n', node.right, '\n')

    def minimum(self):
        return self.min
    
    def extract_min(self):
        min = self.minimum()
        if min.children is None:
            self.consolidate()

        return min.key

    def consolidate(self):
        # Create array indexed by amount of degrees
        max_degree = int(math.log2(self.count)) + 2
        degrees_index = [None] * max_degree

        # Set nodes
        min = self.minimum()
        current_node = min
        next_node = current_node.right

        self.print_root_list()
        # Do While loop
        while True:
            #print(current_node)
            while next_node != min: 
                print(next_node, next_node.right)
                if current_node.degree != next_node.degree:
                    next_node = next_node.right
                    continue
                else:
                   # print("parenting")
                    # Determine new parent and child
                    if current_node.key < next_node.key:
                        child, parent = next_node, current_node
                    else:
                        child, parent = current_node, next_node

                    # Next node's right node
                    next_next_node = next_node.right

                    # Get rid next_node from link chain
                    current_node.right.right.left = current_node
                    current_node.right = current_node.right.right

                    #print(child, parent)

                    if parent.children == None:
                        parent.children = child
                        child.parent = parent
                        child.left = child
                        child.right = child
                    else:
                        child.parent = parent
                        child.right = parent.children
                        child.left = parent.children.left
                        parent.children.left.right = child
                        parent.children.left = child

                    parent.degree += 1
                
                next_node = next_next_node

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
    
    def print_root_list(self):
        if not self.root_list:
            print("Empty root list")
            return

        print("Root list:")
        node = self.root_list
        seen = set()
        while node and node not in seen:
            print(f"Key: {node.key}, Left: {node.left.key}, Right: {node.right.key}")
            seen.add(node)
            node = node.right


fh = FibonacciHeap()
fh.insert(3)
fh.insert(5)
fh.insert(7)
fh.insert(9)
fh.extract_min()
print(fh)