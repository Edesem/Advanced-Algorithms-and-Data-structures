import heapq

def get_freq(s):
    freq = {}

    for c in s:
        if c in freq:
            freq[c] += 1
        else:
            freq[c] = 1

    res = {key: val for key, val in sorted(freq.items(), key = lambda ele: ele[1])}
    print(res)
    return res

def huffman_encode(s):
    f = get_freq(s)
    heap = []

    for key, val in f.items():
        heapq.heappush(heap, (val, key)) 

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)

    print(heap)

huffman_encode("aababbddceef")