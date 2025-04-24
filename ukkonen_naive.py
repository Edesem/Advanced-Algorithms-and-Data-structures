class Node():
    def __init__(self):
        self.children = {}  # char -> (start, end, child_node)
        self.suffix_link = None
        self.parent = None
        self.edge_start = None
        self.edge_end = None

def build_suffix_tree(s):
    s += '$'
    root = Node()
    internal_nodes = []
    
    # Insert suffixes one by one
    for i in range(len(s)):
        current = root
        j = i
        
        while j < len(s):
            next_char = s[j]
            if next_char in current.children:
                start, end, child = current.children[next_char]
                existing_suffix = s[start:end+1]
                k = 0
                    
                # Compare current suffix with the existing suffix
                # s[j] and not char variable because the next_char needs to update
                while k < len(existing_suffix) and j < len(s) and s[j] == existing_suffix[k]:
                    j += 1
                    k += 1

                # If suffix matches
                if k == len(existing_suffix):
                    current = child

                # Else split where the mismatch occurs
                else:
                    split_node = Node()

                    current.children[s[start]] = (start, start + k - 1, split_node)

                    split_node.children[existing_suffix[k]] = (start + k, end, child)
                    split_node.parent = current
                    split_node.edge_start = start
                    split_node.edge_end = start + k - 1
                    
                    internal_nodes.append(split_node)

                    leaf = Node()
                    split_node.children[next_char] = (j, len(s) - 1, leaf)
                    break
                
            # No match, just insert new edge
            else:
                node = Node()
                current.children[next_char] = (j, len(s) - 1, node)
                break
    return root, s

def print_tree(node, text, indent=""):
    for i, (char, (start, end, child)) in enumerate(node.children.items()):
        # get suffix
        suffix = text[start:end + 1]

        # Check to see if its the last child for the branch style
        is_last = (i == len(node.children) - 1)

        # Choose branch
        branch = "└── " if is_last else "├── "
        print(indent + branch + f"[{char}] ({suffix})")

        # Adjust indent level
        next_indent = indent + ("    " if is_last else "│   ")
        print_tree(child, text, next_indent)

s = "abcabxabcd"
root, s = build_suffix_tree(s)
print_tree(root, s)
