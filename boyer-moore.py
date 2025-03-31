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
    """
    Compute R_k(x) for each character x in pattern s.
    Runs in O(|Σ| m) time and space.
    """
    m = len(s)
    alphabet = set(s)  # get alphabet
    hash = defaultdict(lambda: [-1] * m)  

    # Fill table
    for i in range(1, m):  # Start from 1, keeping R_k(x)=-1 for k=0
        char = s[i - 1]  # Previous character (since suffix length is `i`)

        # Copy previous row values
        for c in alphabet:
            hash[c][i] = hash[c][i - 1]  

        # Update current position for char
        hash[char][i] = i - 1  

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
    
    # Debugging info
    print("Bad Character Table:", b_c)
    print("Extended Bad Character Table:")
    for char, shifts in e_b_c.items():
        print(f"  {char}: {shifts}")
    print("Good Suffix Table:", g_s)
    print("Matched Prefix Table:", m_p)

    k = 0
    # While loop so that pattern doesn't overflow the text
    while k <= n-m:
        print(f"\nChecking alignment at index {k}...")
        # Index the last character for pattern
        j = m - 1

        # compare characters from right to left
        while j >= 0 and p[j] == s[k+j]:
            print(f"  Match at pattern[{j}] and text[{k+j}] ({p[j]} == {s[k+j]})")
            j -= 1

        # If pattern is found
        if j == -1:
            print(f"Pattern found at index {k}")
            char = s[k+j] if k + j < n else None
            bad_char_shift = b_c[char] if char else 0

            if k + m < n:
                shift = max(1, bad_char_shift, g_s[j])
                print(f"  Shifting by {shift} (pattern found)")
                k += shift
            else:
                k += 1

        else:
            # Pattern not found, check for bad character
            char = s[k+j]
            print(f"  Mismatch at pattern[{j}] and text[{k+j}] ({p[j]} != {s[k+j]})")
            bad_char_shift = b_c[char]
            extended_bad_char_shift = e_b_c[char][j-1]

            # Clause to prevent negative shifts
            if extended_bad_char_shift == -1:
                extended_bad_char_shift = 0

            # If char does not exist in the pattern, skip past it
            if bad_char_shift == 0:
                print(f"  Character '{char}' not in pattern. Shifting by {m}.")
                k += m
            else:
                shift = max(1, j - bad_char_shift, j - extended_bad_char_shift, g_s[j])
                print(f"  Shifting by {shift} (bad_char_shift={bad_char_shift}, extended_bad_char_shift={extended_bad_char_shift}, good_suffix_shift={g_s[j]})")
                k += shift

s1="acababacaba"
s2="AABAACAADAABAABA"
s3="0011010101111001001101100"

pat1="acab"
pat2="AABA"
pat3="010"

bm(s3, pat3)