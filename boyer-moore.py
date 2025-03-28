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

        if hash[char][i - 1] < n - i:
            hash[char][i - 1] = i - 1

    return hash

def z_suffix(s):
    s = s[::-1]
    
    n = len(s)
    z = [0] * n
    l = r = 0
    found = False

    # Base Case: compute Z[1] from scratch (in 0-based, that's i=1)
    i = 1
    while i < n and s[i] == s[i-1]:
        z[i] += 1
        i += 1
    if z[1] > 0:
        l = 1
        r = z[1]

    # General
    for i in range(2, n): 
        # Case 1: Naive Approach
        if i > r:
            
            # j is prefix
            j = 0
            while i + j < n and s[j] == s[i+j]:
                j += 1
            z[i] = j
            if j > 0:
                l = i
                r = i + (j - 1) # For it was the index before that the right side ends
            #print("case 1:", j)

        # Case 2: In Z-box
        else:
            k = i - l

            # 2a: Copy Previous Z-box
            if z[k] < r - i + 1:
                z[i] = z[k]

            # 2b: Naive Approach outside Z-box
            else:
                j = r + 1
                while j < n and s[j] == s[j-i]:
                    j += 1
                z[i] = j - i
                l = i
                r = j - 1 

    return z[::-1] 

def z_algo(s):
    
    n = len(s)
    z = [0] * n
    l = r = 0
    found = False

    # Base Case: compute Z[1] from scratch (in 0-based, that's i=1)
    i = 1
    while i < n and s[i] == s[i-1]:
        z[i] += 1
        i += 1
    if z[1] > 0:
        l = 1
        r = z[1]

    # General
    for i in range(2, n): 
        # Case 1: Naive Approach
        if i > r:
            
            # j is prefix
            j = 0
            while i + j < n and s[j] == s[i+j]:
                j += 1
            z[i] = j
            if j > 0:
                l = i
                r = i + (j - 1) # For it was the index before that the right side ends
            #print("case 1:", j)

        # Case 2: In Z-box
        else:
            k = i - l

            # 2a: Copy Previous Z-box
            if z[k] < r - i + 1:
                z[i] = z[k]

            # 2b: Naive Approach outside Z-box
            else:
                j = r + 1
                while j < n and s[j] == s[j-i]:
                    j += 1
                z[i] = j - i
                l = i
                r = j - 1 

    return z

def good_suffix(s):
    z = z_suffix(s)

    m = len(s) + 1
    gs = [0] * m
    
    for i in range(m-2):
        gs[m - z[i] - 1] = i

    m = len(s)
    mp = [0] * (m + 1)

    max_z = 0
    for i in reversed(range(1, m + 1)):
        if z[i - 1] == m - i + 1:
            max_z = max(max_z, z[i - 1])
        mp[i - 1] = max_z

    mp[0] = m
        
    return gs, mp
    
def bm(s, p):
    """
    Find R(x)
    """
    n = len(s)
    m = len(p)

    b_c = bad_char(p)
    e_b_c = extended_bad_char(p)
    g_s, m_p = good_suffix(p)
    
    print(b_c)
    for i in e_b_c:
        print(i, e_b_c[i])    
    print(g_s, m_p)

    i = 0
    # While loop so that pattern doesn't overflow the text
    while i <= n-m:
        # Index the last character for pattern
        j = m - 1

        print()
        print("INDEX:",i, j)
        print("COMPARISON:", s[i+j], p[j])

        # compare characters from right to left
        while j >= 0 and p[j] == s[i+j]:
            j -= 1
            print()
            print("COMPARE:", s[i+j], p[j])
            print("crawling", i, j)

        print()
        print("COMPARING:", s[i+j], p[j])

        # If pattern is found
        if j == -1:
            print("Pattern found at index", i)
            char = s[i+j]
            bad_char_shift = b_c[char]
            print("shift", bad_char_shift, g_s[j])
            if i + m < n:
                i += max(1, bad_char_shift, g_s[j])
            else:
                i += 1

        else:
            print("no match")
            char = s[i+j]
            bad_char_shift = b_c[char]
            print("shift", bad_char_shift, g_s[j])
            # If char does not exist in the pattern, skip past it
            if bad_char_shift == 0:
                i += m
            else:
                i += max(1, j - bad_char_shift, g_s[j])

s1="acababacaba"
s2="AABAACAADAABAABA"

pat1="acab"
pat2="AABA"

bm(s1, pat1)