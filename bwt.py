def bwt(s):
    print(s)
    for i in range(1, len(s)):
        print(s[-i:] + s[:-i])

s1 = "wooloomooloo"

bwt(s1)