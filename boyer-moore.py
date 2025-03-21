from collections import defaultdict

def rx(s):
    hash = defaultdict(int)
    n = len(s)
    for i in range(1, n+1):
        print(n-i, hash[s[-i]])
        if hash[s[-i]] < n - i:
            hash[s[-i]] = n - i

    return hash

def rkx(s):
    
        

def bm(s):
    """
    Find R(x)
    """
    rx = rx(s)



bm("acababacaba")