import time

class Node():
    def __init__(self):
        self.children = {}  # char -> (start, end, child_node)
        self.suffix_link = None
        self.parent = None
        self.edge_start = None
        self.edge_end = None

def build_suffix_tree(s):
    # https://www.youtube.com/watch?v=ALEV0Hc5dDk used to supplement knowledge
    root = Node()
    active_node = root
    active_edge = ""
    active_length = 0
    remainder = 0
    last_created_internal_node = None

    for i in range(len(s)):
        remainder += 1
        last_created_internal_node = None

        while remainder > 0:
            if active_length == 0:
                active_edge = s[i]

            if active_edge not in active_node.children:
                # Create new leaf
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
                    active_node = next_node
                    active_length -= edge_length
                    active_edge = s[start + edge_length]
                    continue

                if s[start + active_length] == s[i]:
                    active_length += 1
                    if last_created_internal_node:
                        last_created_internal_node.suffix_link = active_node
                    break
                else:
                    # Split edge
                    split = Node()
                    split.edge_start = start
                    split.edge_end = start + active_length - 1

                    leaf = Node()
                    leaf.edge_start = i
                    leaf.edge_end = len(s) - 1

                    active_node.children[active_edge] = (split.edge_start, split.edge_end, split)
                    split.children[s[start + active_length]] = (start + active_length, end, next_node)
                    split.children[s[i]] = (i, len(s) - 1, leaf)

                    if last_created_internal_node:
                        last_created_internal_node.suffix_link = split
                    last_created_internal_node = split

            remainder -= 1

            if active_node == root and active_length > 0:
                active_length -= 1
                active_edge = s[i - remainder + 1] if remainder > 0 else ""
            elif active_node != root:
                active_node = active_node.suffix_link if active_node.suffix_link else root

    return root

def naive_suffix_tree(s):
    root = Node()
    for i in range(len(s)):
        current = root
        j = i

        while j < len(s):
            next_char = s[j]
            if next_char in current.children:
                start, end, child = current.children[next_char]
                label = s[start:end + 1]
                active_length = 0

                # Traverse along the edge until mismatch or end
                while active_length < len(label) and j < len(s) and s[j] == label[active_length]:
                    j += 1
                    active_length += 1

                if active_length == len(label):
                    current = child
                else:
                    # Mismatch – need to split
                    split = Node()
                    split.edge_start = start
                    split.edge_end = start + active_length - 1
                    split.parent = current

                    # Update old child
                    child.edge_start = start + active_length
                    split.children[s[child.edge_start]] = (child.edge_start, end, child)
                    child.parent = split

                    # Create new leaf
                    leaf = Node()
                    leaf.edge_start = j
                    leaf.edge_end = len(s) - 1
                    split.children[s[j]] = (j, len(s) - 1, leaf)
                    leaf.parent = split

                    # Reassign split to parent
                    current.children[next_char] = (split.edge_start, split.edge_end, split)
                    break
            else:
                # No match – insert new leaf
                leaf = Node()
                leaf.edge_start = j
                leaf.edge_end = len(s) - 1
                current.children[next_char] = (j, len(s) - 1, leaf)
                leaf.parent = current
                break

    return root

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

def preformance():
    s = "bananabanana" * 1000 + "$" 

    start = time.time()
    root = build_suffix_tree(s)
    end = time.time()
    #print_tree(root, s)

    print(f"Ukkonen: {end - start:.6f} seconds")


    start = time.time()
    root = naive_suffix_tree(s)
    end = time.time()
    #print_tree(root, s)

    print(f"Naive: {end - start:.6f} seconds")
