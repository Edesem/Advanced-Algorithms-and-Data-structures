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
    
    last_col = bwt_key(bwt)
    
    last_col = char_rank(last_col)
    #sorted_k = "".join(sorted(k))
    first_col = sorted(last_col, key=lambda x: x[0])  # Sort by rank (second element)
    
    for i in range(len(last_col)):
        print(first_col[i], last_col[i])
    
    # Start at $
    str=""
    previous_char = "$"
    previous_rank = 1
    while len(str) < len(last_col):
        for i in range(len(last_col)):
            first_char, first_rank = first_col[i]
            last_char, last_rank = last_col[i]


            if last_char == previous_char and last_rank == previous_rank:
                str += first_char
                previous_char = first_char
                previous_rank = first_rank
                break

    print(str)
        

s1 = "wooloomooloo$"
s2 = "olba$luaolh"

bwt_a = bwt_array(s1)

for i in bwt_a:
    print(i)
print()
bwt_invert(bwt_a)
