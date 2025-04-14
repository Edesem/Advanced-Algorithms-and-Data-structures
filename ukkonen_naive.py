class Node:
    def __init__(self):
        self.children = {}  # char -> (start, end, child_node)

def build_naive_suffix_tree(text):
    text += '$'
    root = Node()
    for i in range(len(text)):
        current = root
        j = i
        while j < len(text):
            if text[j] in current.children:
                start, end, child = current.children[text[j]]
                label = text[start:end+1]
                k = 0
                while k < len(label) and j < len(text) and text[j] == label[k]:
                    j += 1
                    k += 1
                if k == len(label):
                    current = child
                else:
                    # Need to split
                    split_node = Node()
                    current.children[text[start]] = (start, start + k - 1, split_node)
                    split_node.children[label[k]] = (start + k, end, child)
                    leaf = Node()
                    split_node.children[text[j]] = (j, len(text) - 1, leaf)
                    break
            else:
                leaf = Node()
                current.children[text[j]] = (j, len(text) - 1, leaf)
                break
    return root, text

def print_tree(node, text, indent=""):
    for i, (char, (start, end, child)) in enumerate(node.children.items()):
        label = text[start:end + 1]
        is_last = (i == len(node.children) - 1)
        branch = "└── " if is_last else "├── "
        print(indent + branch + f"[{char}] ({label})")
        next_indent = indent + ("    " if is_last else "│   ")
        print_tree(child, text, next_indent)


if __name__ == '__main__':
    text = 'banana'
    tree, full_text = build_naive_suffix_tree(text)
    print_tree(tree, full_text)

