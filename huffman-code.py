import heapq
from itertools import count

def get_freq(s):
    freq = {}
    for c in s:
        freq[c] = freq.get(c, 0) + 1
    return {key: val for key, val in sorted(freq.items(), key=lambda ele: ele[1])}

def print_huffman_tree(node, indent="", is_left=True):
    freq, _, data = node
    if isinstance(data, str):
        print(f"{indent}{'├── ' if is_left else '└── '}'{data}' ({freq})")
    else:
        print(f"{indent}{'├── ' if is_left else '└── '}* ({freq})")
        left, right = data
        print_huffman_tree(left, indent + ("│   " if is_left else "    "), True)
        print_huffman_tree(right, indent + ("│   " if is_left else "    "), False)

def huffman_encode(s):
    f = get_freq(s)
    print("Frequencies:", f)
    heap = []
    counter = count()

    for key, val in f.items():
        heapq.heappush(heap, (val, next(counter), key))

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        combined_freq = left[0] + right[0]
        new_node = (combined_freq, next(counter), (left, right))
        heapq.heappush(heap, new_node)

    root = heap[0]
    print("\nFinal Huffman Tree:")
    print_huffman_tree(root)

huffman_encode("aababbddceef")
