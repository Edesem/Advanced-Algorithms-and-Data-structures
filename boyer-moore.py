from collections import defaultdict

def bad_char(s):
    hash = defaultdict(int)
    n = len(s)
    for i in range(1, n+1):
        char = s[-i]

        if hash[char] < n - i:
            hash[char] = n - i

    return hash

def extended_bad_char(s):
    n = len(s)
    hash = defaultdict(lambda: [0] * (n - 1))

    for i in range(1, n):
        suffix = s[:i]
        char = suffix[i - 1]
        print(suffix)

        if hash[char][i - 1] < n - i:
            hash[char][i - 1] = i - 1

    return hash

        

def bm(s):
    """
    Find R(x)
    """
    print(extended_bad_char(s))


s1="acababacaba"
s2="tbapxab"

bm(s2)