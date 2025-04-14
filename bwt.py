def bwt_array(s):
    bwt = []
    
    bwt.append(s)
    for i in range(1, len(s)):
        bwt.append(s[-i:] + s[:-i])

    return bwt

def bwt_key(bwt):
    s = bwt[0]
    bwt.sort()

    key = ""

    for i in range(len(s)):
        key += bwt[i][-1]

    return key

def bwt_invert(bwt):
    # Thought, what if I used a hashmap with a linked list for the character match?

    def char_rank(s):
        count = {}  # Dictionary to track occurrences
        ranked = []

        for char in s:
            count[char] = count.get(char, 1) + 1  # Increment count
            ranked.append((char, count[char] - 1))  # Assign occurrence rank

        return ranked
    
    k = bwt_key(bwt)

    k = char_rank(k)
    #sorted_k = "".join(sorted(k))
    sorted_k = sorted(k, key=lambda x: x[0])  # Sort by rank (second element)
    
    for i in range(len(k)):
        print(sorted_k[i], k[i])

    
    # Start at $
    str=""
    for i in range(len(k)):
        if k[i][0] == "$":
            str = sorted_k[i][0]
        
    




s1 = "wooloomooloo$"
s2 = "olba$luaolh"

bwt_a = bwt_array(s1)

for i in bwt_a:
    print(i)
print()
bwt_invert(bwt_a)
