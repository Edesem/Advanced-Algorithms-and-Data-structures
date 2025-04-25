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
    active_node = root
    active_edge = None
    active_length = 0
    remainder = 0
    last_created_internal_node = None
    
    # Insert suffixes one by one
    for i in range(len(s)):
        remainder += 1
        last_created_internal_node = None

        while remainder > 0:
            if active_length == 0:
                active_edge = s[i]
            
            if active_edge not in active_node.children: # WHAT ARE THE CHILDREN LOOKING LIKE?
                # Create a new leaf
                leaf = Node()
                leaf.edge_start = i
                leaf.edge_end = len(s) - 1
                active_node.children[active_edge] = (i, len(s) - 1, leaf)

                if last_created_internal_node:
                    last_created_internal_node.suffix_link = active_node
                    last_created_internal_node = None
            else:
                start, end, next_node = active_node.children[active_edge]
                edge_length = end - start + 1
                if active_length >= edge_length:
                    # Walk down
                    active_node = next_node
                    active_length -= edge_length
                    active_edge = s[i - remainder + 1 + edge_length]
                    continue

                if s[start + active_length] == s[i]:
                    # Just extend the path
                    active_length += 1
                    if last_created_internal_node:
                        last_created_internal_node.suffix_link = active_node
                    break  # No more remainder handling this phase
                else:
                    # Split the edge
                    split = Node()
                    split.edge_start = start
                    split.edge_end = start + active_length - 1

                    leaf = Node()
                    leaf.edge_start = i
                    leaf.edge_end = len(s) - 1

                    # Update split edges
                    active_node.children[active_edge] = (split.edge_start, split.edge_end, split)
                    split.children[s[start + active_length]] = (start + active_length, end, next_node)
                    split.children[s[i]] = (i, len(s) - 1, leaf)

                    # Save suffix link
                    if last_created_internal_node:
                        last_created_internal_node.suffix_link = split
                    last_created_internal_node = split

            remainder -= 1

            if active_node == root and active_length > 0:
                active_length -= 1
                active_edge = s[i - remainder + 1]
            elif active_node.suffix_link:
                active_node = active_node.suffix_link
            else:
                active_node = root


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
