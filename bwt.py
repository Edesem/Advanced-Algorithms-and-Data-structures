def bwt(s):
    bwt = []
    
    bwt.append(s)
    for i in range(1, len(s)):
        bwt.append(s[-i:] + s[:-i])

    return bwt

s1 = "wooloomooloo"

bwt_a = bwt(s1)

for i in bwt_a:
    print(i)