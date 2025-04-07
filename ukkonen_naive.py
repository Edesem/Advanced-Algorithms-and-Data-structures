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
    def __init__(self):
        self.children = {}  # Dictionary to store edges (key: character, value: Node)
        self.start = None  # Start index of substring (for edge label)
        self.end = None  # End index of substring

class SuffixTree:
    def __init__(self, text):
        self.text = text
        self.root = Node()  # Root of the tree
        self.build_tree()

    def build_tree(self):
        """Naively build the suffix tree by inserting all suffixes."""
        for i in range(len(self.text)):  # Insert each suffix into the tree
            self.insert_suffix(i)

    def insert_suffix(self, suffix_start):
        """Insert a suffix starting at index `suffix_start`."""
        current_node = self.root
        i = suffix_start  # Start of suffix

        while i < len(self.text):
            char = self.text[i]

            if char not in current_node.children:
                # Create a new node for this character
                new_node = Node()
                new_node.start = i
                new_node.end = len(self.text)  # End of substring
                current_node.children[char] = new_node
                return  # Suffix is fully inserted

            # If character exists, follow the edge
            current_node = current_node.children[char]
            i += 1  # Move to next character

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
            # end of extension j
        # end of phase i+1 (I_{i+1} computed)
    return tree

# Example usage
if __name__ == "__main__":
    text = "abac"
    suffix_tree = naive_suffix_tree(text)
    suffix_tree.print_tree()
    # Output the suffix tree structure
    # This will print the structure of the suffix tree for the given text
    # Note: The print_tree method is a simple representation of the tree.
    # Expected output:
    # └── [b] (banana)
    #     └── [a] (ana)