import time

class Node():
    def __init__(self):
        self.children = {}  # char -> edge
        self.suffix_link = None
        self.parent = None

class Edge():
    def __init__(self, start, end, child):
        self.start = start
        self.end = end 
        self.child = child

def build_suffix_tree(s):
    # https://www.youtube.com/watch?v=ALEV0Hc5dDk used to supplement knowledge
    root = Node()
    active_node = root
    active_edge = ""
    active_length = 0
    remainder = 0  # Number of suffixes to add
    last_created_internal_node = None
    global_end = [-1] # Shared pointer for all leaves, to allow for rapid leaf extension

    for i in range(len(s)):
        global_end[0] = i # Extend the leaves at once
        remainder += 1
        last_created_internal_node = None

        # Number of characters left to add
        while remainder > 0:
            if active_length == 0:
                active_edge = s[i]

            if active_edge not in active_node.children:
                # Create new leaf
                leaf = Node()
                active_node.children[active_edge] = Edge(i, global_end, leaf)

                if last_created_internal_node:
                    last_created_internal_node.suffix_link = active_node
                    last_created_internal_node = None
            else:
                edge = active_node.children[active_edge]
                start = edge.start
                end = edge.end
                next_node = edge.child
                
                # Prevent TypeError
                if isinstance(end, list):
                    edge_length = end[0] - start + 1
                else:
                    edge_length = end - start + 1

                # Skip counting
                # Jump node and subtract edge_length from active_length
                # Instead of traversing one by one
                if active_length >= edge_length:
                    active_node = next_node
                    active_length -= edge_length
                    active_edge = s[start + edge_length]
                    continue

                # Does the next character already exist from the root?
                # Make Extension
                if s[start + active_length] == s[i]:
                    active_length += 1
                    if last_created_internal_node:
                        last_created_internal_node.suffix_link = active_node
                    break # Show stopper rule
                else:
                    # Split edge
                    split = Node()
                    active_node.children[active_edge] = Edge(start, start + active_length - 1, split)

                    leaf = Node()
                    split.children[s[start + active_length]] = Edge(start + active_length, end, next_node)
                    split.children[s[i]] = Edge(i, global_end, leaf)

                    # suffix link
                    if last_created_internal_node:
                        last_created_internal_node.suffix_link = split
                    last_created_internal_node = split

            remainder -= 1

            # Move to next extension
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
    #s = "bananabanana" * 1000 + "$" 
    s = "abcabxabcd$"

    start = time.time()
    root = build_suffix_tree(s)
    end = time.time()
    print_tree(root, s)

    print(f"Ukkonen: {end - start:.6f} seconds")


    start = time.time()
    root = naive_suffix_tree(s)
    end = time.time()
    #print_tree(root, s)

    print(f"Naive: {end - start:.6f} seconds")

#preformance()