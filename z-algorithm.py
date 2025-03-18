def z(str):
    """
    3 Cases

    Base case. Compare each character, beginning with Z[1] and Z[0] till mismatch occurs

    1. i > r
        - i > r means i is outside the current z-box
        - So we have to start from scratch and compare str[0:] with str[i:]

    2. i <= r
        - i <= r means i is inside the current z-box
        - So we can use the previous z values to calculate z[i]
        - k = i - l

        2a. z[k] < r - l 
            - case when you copy the z values from the previous box to current box whilst the rule applies
        2b. z[k] >= r - l
            - case when you have to compare characters one by one
            - j = r + 1
            - start comparing outside of the z-box str[j] with str[j-i] until a mismatch occurs
            - say mismatch happens at m
            - set Z[i] = m - i
            - set l = i
            - set r = m - 1
    """
    n = len(str)
    z = [0] * n
    l = r = 0
    found = False

    # Base Case: compute Z[1] from scratch (in 0-based, that's i=1)
    i = 1
    while i < n and str[i] == str[i-1]:
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
            while i + j < n and str[j] == str[i+j]:
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
                #print("case 2a:")

            # 2b: Naive Approach outside Z-box
            else:
                j = r + 1
                while j < n and str[j] == str[j-i]:
                    j += 1
                z[i] = j - i
                l = i
                r = j - 1 
                #print("case 2b:", j, i, str[j-i], str[j-1])

        #print(l, r, i)
        #print(z)
                

    print("Final:", z)

str = "abababa"
str1 = "aabcaabxaaaz"
str2 = "aabzaabzcaabzaabza"
str3 = "aabb#abcdeaabbdfaabdfg"

z(str2)

