import heapq

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
    heap = []
    counter = 0

    for key, val in f.items():
        counter += 1
        heapq.heappush(heap, (val, counter, key))

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)

        combined_freq = left[0] + right[0]
        counter += 1

        new_node = (combined_freq, counter, (left, right))
        heapq.heappush(heap, new_node)
        
    print("\nFinal Huffman Tree:")
    print_huffman_tree(heap[0])
    huffman_coding(heap[0])

def huffman_coding(node, code=""):
    _, _, data = node
    if isinstance(data, str):
        print(f"{data}: {code}")
    elif isinstance(data, tuple):
        left, right = data
        huffman_coding(left, code + "0")
        huffman_coding(right, code + "1")

    

s = "A" * 5 + "B" * 9 + "C" * 12 + "D" * 13 + "E" * 16 + "F" * 45
s1 = "aaaabbccde"
huffman_encode(s1)
