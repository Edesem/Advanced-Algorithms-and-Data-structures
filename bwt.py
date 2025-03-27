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

s1 = "wooloomooloo"

bwt_a = bwt_array(s1)

for i in bwt_a:
    print(i)

bwt_k = bwt_key(bwt_a)

print()
print(bwt_k)