"""
1 implicit_suffix_tree(str):
    2 n = len(str)
    3 Construct I_1
    4 for i from 1 to n-1:
        5 # begin phase i+1
        6 for j from 1 to i+1:
            7 # begin extension j
            8 Follow the path str[j...i] from the root in the current state of the implicit suffix tree.
            9 Apply the appropriate suffix extension rule.
    10 # str[j...i+1] is now in the tree
11 # end of phase i+1 (I_{i+1} computed)
"""

class Node:
    def __init__(self, start=None, end=None):
        self.children = {}  # Key: first char of the edge label
        self.start = start  # Index in original text
        self.end = end      # Index in original text

class SuffixTree:
    def __init__(self, text):
        self.text = text
        self.root = Node()  # Root of the tree
        self.build_tree()

    def build_tree(self):
        n = len(self.text)
        for i in range(n):  # Phase i+1
            for j in range(i + 1):  # Extensions
                self.insert_suffix(j, i)

    def insert_suffix(self, start_index, end_index):
        """Insert the suffix text[start_index:end_index+1] into the tree."""
        current_node = self.root
        k = start_index  # Cursor in the suffix

        while k <= end_index:
            current_char = self.text[k]
            if current_char not in current_node.children:
                # No edge starting with current_char, create a new leaf
                leaf = Node(k, end_index + 1)
                current_node.children[current_char] = leaf
                return

            child = current_node.children[current_char]
            edge_start = child.start
            edge_end = child.end
            label = self.text[edge_start:edge_end]
            l = 0  # Match length

            # Walk along the edge label
            while k <= end_index and l < len(label) and self.text[k] == label[l]:
                k += 1
                l += 1

            if l == len(label):
                # Full match, descend to the child
                current_node = child
            else:
                # Mismatch — split the edge
                split = Node(edge_start, edge_start + l)
                current_node.children[current_char] = split

                # Adjust the original child
                child.start = edge_start + l
                split.children[self.text[child.start]] = child

                # Add the new leaf for the remaining suffix
                new_leaf = Node(k, end_index + 1)
                split.children[self.text[k]] = new_leaf
                return

    def print_tree(self, node=None, indent=""):
        """Recursively print the tree structure."""
        if node is None:
            node = self.root
        for char, child in node.children.items():
            print(indent + f"└── [{char}] ({self.text[child.start:child.end]})")
            self.print_tree(child, indent + "    ")


def naive_suffix_tree(str):
    n = len(str)
    tree = SuffixTree(str)
    root = Node()
    tree.root = root

    for i in range(n):
        # begin phase i+1
        for j in range(i + 1):
            # begin extension j
            current_node = root
            k = j
            while k <= i:
                char = str[k]
                if char not in current_node.children:
                    # Create a new node for this character
                    new_node = Node()
                    new_node.start = k
                    new_node.end = n
                    current_node.children[char] = new_node
                    break
                # If character exists, follow the edge
                current_node = current_node.children[char]
                k += 1

                print(f"Following edge for {char}: {str[current_node.start:current_node.end]}")
            # end of extension j
        # end of phase i+1 (I_{i+1} computed)
    return tree
    
# Example usage
if __name__ == "__main__":
    text = "banana"
    suffix_tree = naive_suffix_tree(text)
    suffix_tree.print_tree()
    # Output the suffix tree structure
    # This will print the structure of the suffix tree for the given text
    # Note: The print_tree method is a simple representation of the tree.
    # Expected output:
    # └── [b] (banana)
    #     └── [a] (ana)