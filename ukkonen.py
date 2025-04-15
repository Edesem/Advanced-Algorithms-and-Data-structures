class Node():
    def __init__(self):
        self.children = {}  # char -> (start, end, child_node)

def build_suffix_tree(s):
    s += '$'
    root = Node()
    
    # Insert suffixes one by one
    for i in range(len(s)):
        current = root
        j = i
        
        while j < len(s):
            char = s[j]
            if char in current.children:
                start, end, child = current.children[char]
                suffix = s[start:end+1]
                k = 0
                    
                # Compare for 
                while s[j] == suffix[k] and k < len(suffix):
                    j += 1
                    k += 1

                # If suffix matches
                if k == len(suffix):
                    current = child

                # Else split where the mismatch occurs
                else:
                    split_node = Node()
                    
                    current.children[s[start]] = (start, start + k - 1, split_node)
                    split_node.children[suffix[k]] = (start + k, end, child)

                    leaf = Node()
                    split_node.children[s[j]] = (j, len(s) - 1, leaf)
                    break
        print(s[i:])

build_suffix_tree("banana")