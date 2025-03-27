def bwt(s):
    bwt = []
    
    bwt.append(s)
    for i in range(1, len(s)):
        bwt.append(s[-i:] + s[:-i])

    bwt.sort()

    key = ""

    for i in range(len(s)):
        print(bwt[i][-1])
        key += bwt[i][-1]

    return key

s1 = "wooloomooloo"

bwt_a = bwt(s1)

print(bwt_a)