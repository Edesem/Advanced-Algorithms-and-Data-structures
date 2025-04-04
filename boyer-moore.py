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
    # corner case
    if p == "" or t == "":
        return []

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

    j = 0
    # While loop so that pattern doesn't overflow the text
    while j <= n-m:
        print(f"\nChecking alignment at index {j}...")
        # Index the last character for pattern
        k = m - 1

        # compare characters from right to left
        while k >= 0 and p[k] == s[j+k]:
            print(f"  Match at pattern[{k}] and text[{j+k}] ({p[k]} == {s[j+k]})")
            k -= 1

        # If pattern is found
        if k == -1:
            print(f"\n\nPATTERN FOUND AT {j}\n\n")
            char = s[j+m] if j + m < n else None
            bad_char_shift = b_c[char] - 1 if char else 0
            extended_bad_char_shift = e_b_c[char][k-1] - 1 if char else 0

            # Clause to prevent negative shifts
            if extended_bad_char_shift == -1:
                extended_bad_char_shift = 0

            if j + m < n:
                shift = max(1, m_p[k], g_s[k])
                print(m_p[k], g_s[k])
                print(f"  Shifting by {shift} (pattern found)")
                j += shift
            else:
                j += 1

        else:
            # Pattern not found, check for bad character
            char = s[j+k]
            print(f"  Mismatch at pattern[{k}] and text[{j+k}] ({p[k]} != {s[j+k]})")
            bad_char_shift = b_c[char]
            extended_bad_char_shift = e_b_c[char][k-1]

            method = max(bad_char_shift, extended_bad_char_shift)

            # If char does not exist in the pattern, skip past it
            if bad_char_shift == -1:
                print(f"  Character '{char}' not in pattern. Shifting by {m-(m-(k+1))}.")
                j += (m - (m - (k + 1)))
            else:
                # Check if mismatched character appears further in the pattern
                if bad_char_shift == -1 or bad_char_shift > k:
                    # If it doesn't appear, shift past the mismatch
                    print(f"  Character '{char}' does not appear later in the pattern. Shifting by {m-(k+1)}.")
                    j += m - (k + 1)
                else:
                    shift = max(1, k - method, g_s[k])
                    if bad_char_shift > k:
                        shift = 1
                    print(f"  Shifting by {shift}, k is {k} (bad_char_shift={bad_char_shift}, extended_bad_char_shift={extended_bad_char_shift}, good_suffix_shift={g_s[k]})")
                    j += shift

s1="acababacaba"
s2="AABAACAADAABAABA"
s3="0011010101111001001101100"
s4="abcabcabc"
s5="111000111"


pat1="acab"
pat2="AABA"
pat3="010"
pat4="abc"
p5="111"

#bm(s1, pat1)
#bm(s2, pat2)
#bm(s3, pat3)
#bm(s4, pat4)
bm(s5, p5)